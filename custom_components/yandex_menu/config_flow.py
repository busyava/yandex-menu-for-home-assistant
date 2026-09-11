"""Настройка интеграции: одна кнопка, без полей."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DOMAIN, PANEL_TITLE, YS_DOMAIN


class YandexDevicesConfigFlow(ConfigFlow, domain=DOMAIN):
    """Проверяем, что есть Яндекс.Станция, и создаём запись."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if not self.hass.config_entries.async_entries(YS_DOMAIN):
            return self.async_abort(reason="no_yandex_station")

        if user_input is not None:
            return self.async_create_entry(title=PANEL_TITLE, data={})

        return self.async_show_form(step_id="user")
