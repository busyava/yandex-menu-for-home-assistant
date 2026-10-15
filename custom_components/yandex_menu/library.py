"""Чтение файловой библиотеки Music Assistant без отдельного клиента."""
from __future__ import annotations

import asyncio
import inspect
import re
from typing import Any

PAGE_SIZE = 200
SCAN_TIMEOUT = 300
FILE_PROVIDERS = {"filesystem_local", "filesystem_smb"}


def _get(obj: Any, key: str, default=None):
    return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)


def get_mass(hass):
    """Вернуть клиент только загруженной записи интеграции MA."""
    try:
        for entry in hass.config_entries.async_entries("music_assistant"):
            if _get(entry.state, "value", entry.state) != "loaded":
                continue
            if mass := getattr(getattr(entry, "runtime_data", None), "mass", None):
                return mass
    except (AttributeError, TypeError):
        pass
    return None


def _providers(mass):
    return [p for p in mass.providers if _get(p, "domain") in FILE_PROVIDERS]


def _parts(path):
    if not isinstance(path, str) or path.startswith(("/", "\\")):
        return []
    parts = path.replace("\\", "/").split("/")
    if not parts or any(not p or p.startswith(("_", ".")) for p in parts):
        return []
    return parts


def clean_title(value, *, audiobook=False):
    """Убрать технические метки и чтеца из имени коллекции."""
    title = str(value).replace("---", "—")
    title = re.sub(r"\[[^]\n]*\]", " ", title)
    title = re.sub(r"\b\d{4}-\d{2}-\d{2}\b|\(\d{4}\)", " ", title)
    title = re.sub(r"\b(?:\d{2,4}\s*(?:kbps|кбит(?:/с)?|kb/s)|FLAC|MP3)\b", " ", title, flags=re.I)
    title = re.sub(r"\s*\([^()]*\)\s*$", "", title)
    if audiobook and " — " in title:
        title = title.split(" — ", 1)[1]
    title = " ".join(re.sub(r"[\W_]", " ", title).split())
    return " ".join(title.split()[:6])[:60].rstrip()


def _sort_album(row):
    name = row["path"][1] if len(row["path"]) > 1 else row["path"][0]
    date = re.search(r"\d{4}-\d{2}-\d{2}", name)
    return (date.group() if date else name.casefold(), name.casefold(), row["uri"])


async def read_library(mass) -> dict:
    """Получить полный снимок; неполный снимок нельзя применять к карточкам."""
    result = {"complete": False, "launches": [], "providers": [], "error": None,
              "sources_healthy": False, "sources": {}, "warnings": [], "skipped_keys": []}
    if mass is None:
        result["error"] = "Music Assistant недоступен"
        return result
    try:
        providers = _providers(mass)
        ids = {_get(p, "instance_id") for p in providers}
        source_names = {_get(p, "instance_id"): _get(p, "name") or _get(p, "domain") for p in providers}
        result["providers"] = sorted(ids)
        source_health = {_get(p, "instance_id"): bool(_get(p, "available", False))
                         for p in providers}
        grouped = {}
        objects = {p: set() for p in ids}
        for kind, method in (("album", mass.music.get_library_albums),
                             ("audiobook", mass.music.get_library_audiobooks)):
            offset = 0
            while True:
                page = await method(limit=PAGE_SIZE, offset=offset, order_by="sort_name")
                for item in page:
                    uri = _get(item, "uri")
                    if not uri:
                        raise ValueError("MA вернул объект без URI")
                    for mapping in _get(item, "provider_mappings", ()):
                        provider = _get(mapping, "provider_instance")
                        if provider not in ids:
                            continue
                        objects[provider].add((kind, uri))
                        if not _get(mapping, "available", True):
                            source_health[provider] = False
                        parts = _parts(_get(mapping, "item_id"))
                        if not parts:
                            continue
                        # У книги путь указывает на первую главу, у альбома — на папку.
                        if kind == "audiobook" and len(parts) < 2:
                            continue
                        # У ProviderInstance нет content_type: используем тип объекта.
                        # Второй сегмент используем ниже только для нескольких книг
                        # автора: у одной книги это может быть папка диска с главами.
                        folder = parts[0]
                        grouped.setdefault((provider, folder), []).append({
                            "kind": kind, "path": parts, "uri": uri,
                            "title": _get(item, "name", parts[0]),
                            "identity": f"{provider}|{_get(item, 'item_id')}",
                        })
                offset += len(page)
                if len(page) < PAGE_SIZE:
                    break
        # Собираем книги одной верхней папки до формирования ключей: автор
        # может содержать одновременно однофайловые книги и папки с главами.
        books_by_top = {}
        for (provider, _), rows in grouped.items():
            for row in rows:
                if row["kind"] == "audiobook":
                    books_by_top.setdefault((provider, row["path"][0]), set()).add(row["uri"])
        regrouped = {}
        for (provider, folder), rows in grouped.items():
            for row in rows:
                row_folder = folder
                if (row["kind"] == "audiobook"
                        and len(books_by_top[(provider, row["path"][0])]) > 1):
                    row_folder = "/".join(row["path"][:2])
                regrouped.setdefault((provider, row_folder), []).append(row)
        launches = []
        for (provider, top), rows in sorted(regrouped.items()):
            # Один объект может иметь несколько mappings в одной верхней папке.
            rows = list({(r["kind"], r["uri"]): r for r in rows}.values())
            albums = [r for r in rows if r["kind"] == "album"]
            subfolders = {r["path"][1] for r in albums if len(r["path"]) > 1}
            if (len(subfolders) >= 2 and all(len(r["path"]) > 1 for r in albums)
                    and len(albums) == len(rows)):
                media = {"media_type": "folder_artist", "uris": [r["uri"] for r in sorted(albums, key=_sort_album)]}
                title = top
                ordered_albums = sorted(albums, key=_sort_album)
            elif len(rows) == 1:
                media = {"media_type": rows[0]["kind"], "uri": rows[0]["uri"]}
                title = rows[0]["title"]
            else:
                # Не выбираем случайную книгу/альбом при неоднозначной раскладке.
                key = f"{provider}|{top}"
                result["skipped_keys"].append(key)
                result["warnings"].append({
                    "key": key, "folder": top, "reason": "несколько книг/альбомов",
                    "provider_instance": provider,
                    "identities": sorted({r["identity"] for r in rows}),
                })
                continue
            launches.append({"source": "library", "key": f"{provider}|{top}", "title": clean_title(title, audiobook=media["media_type"] == "audiobook") or clean_title(top),
                             "source_name": source_names[provider],
                             "albums": [{"title": clean_title(r["title"]) or clean_title(r["path"][-1]), "uri": r["uri"]} for r in ordered_albums] if media["media_type"] == "folder_artist" else [],
                             "media": media, "provider_instance": provider,
                             "identities": sorted({r["identity"] for r in rows})})
        result.update(complete=True, launches=launches,
                      sources_healthy=bool(ids) and all(source_health[p] and objects[p] for p in ids),
                      sources={p: {"healthy": source_health[p] and bool(objects[p]),
                                   "items": len(objects[p])} for p in sorted(ids)})
    except Exception as err:
        result["error"] = str(err) or type(err).__name__
    return result


async def scan_library(mass, progress=None) -> dict:
    """Запросить скан и дождаться его событий, а не только ответа music/sync."""
    result = {"scan_requested": False, "scheduled": True, "error": None}
    if mass is None:
        result["error"] = "Music Assistant недоступен"
        return result
    unsubscribe = None
    try:
        providers = [_get(p, "instance_id") for p in _providers(mass)]
        if not providers:
            result["error"] = "Нет файловых источников Music Assistant"
            return result
        changed = asyncio.Event()
        tasks = None
        seen_running = False

        def updated(event):
            nonlocal tasks, seen_running
            data = _get(event, "data")
            if not isinstance(data, list):
                return
            tasks = [t for t in data if _get(t, "provider_instance") in providers]
            seen_running = seen_running or bool(tasks)
            changed.set()

        # Подписка до команды: короткий скан может закончиться раньше ответа.
        unsubscribe = mass.subscribe(updated, ("sync_tasks_updated",))
        async with asyncio.timeout(SCAN_TIMEOUT):
            await mass.music.start_sync(media_types=["track", "audiobook"], providers=providers)
            result["scan_requested"] = True
            while True:
                await changed.wait()
                changed.clear()
                if progress:
                    value = progress({"stage": "scan", "tasks": len(tasks)})
                    if inspect.isawaitable(value):
                        await value
                if seen_running and not tasks:
                    result["scheduled"] = False
                    return result
    except TimeoutError:
        result["error"] = "Не удалось дождаться завершения скана Music Assistant"
    except Exception as err:
        result["error"] = str(err) or type(err).__name__
    finally:
        if unsubscribe:
            unsubscribe()
    return result
