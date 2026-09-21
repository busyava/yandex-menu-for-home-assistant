# Yandex Menu for Home Assistant

[Русская версия](README.md)

A **Яндекс меню** ("Yandex menu") item in the Home Assistant sidebar that gathers every device in
your Yandex home, together with the things you normally have to open the Yandex app ("Дом с
Алисой") for: what a device is called by voice, which room it is in, and which lamp comes on when
you say "Alice, turn on the light".

No separate Yandex login is needed — the integration uses the same access that
[Yandex Station](https://github.com/AlexxIT/YandexStation) already has.

![The Yandex menu panel in Home Assistant: a Yandex home listed room by room, every device with icons for what it can do, and an open device card showing the words to say to Alice](https://raw.githubusercontent.com/busyava/yandex-menu-for-home-assistant/main/docs/panel.png)

One thing to know before you start: the panel itself is in Russian, just as in the screenshot
above. Only the setup and options dialogs are translated. So buttons and sections are named here in
English, with the Russian original — the one you will see on screen — in brackets, and messages
from the panel are quoted in Russian, with what they mean in brackets.

## Why you might need it

A home collects a dozen devices over time, and the hard part is remembering what they are called.
To switch off one lamp in the living room you start guessing: "Alice, turn off the chandelier" —
wrong one, "turn off the ambient light" — wrong again. The names live in the Yandex app, and you
are at the computer, in Home Assistant.

The panel shows everything at once: one click in the sidebar and there is the whole list by room —
every device your Yandex home knows about and what each of them is called by voice. The
Home Assistant entity the device is linked to is right there next to it. No need to reach for the
phone.

From there you can simply look a name up, or fix it on the spot: give a device a name that makes
sense, or add synonyms so it answers to whichever variant comes to mind first. If you cannot tell
which lamp you are looking at, the **blink** button (Проверить: мигнуть) turns it on for three
seconds.

That familiar "Alice, turn on the light", which lights up the whole room at once, is fixed here
too — that is what the main and secondary light roles on a lamp are for.

## Features

### Names, rooms and the light role

- **Voice names.** Up to five per device. The panel warns you when a new name duplicates another
  one or overlaps it: when one name sits inside another ("Ambient light" inside "Sofa ambient
  light"), Alice acts on the shorter one.
- **Main and secondary light.** The role switch — the fix for "turn on the light". Yandex lets you
  change the role only on some lamps — where it cannot be changed, the card simply has no switch.
- **Room** (Комната). Moves a device between Yandex rooms — the same ones you have in the Yandex
  app.

### Voice commands

- **What to say to Alice.** For every device you can see what it can do and the words that go into
  commands: brightness, colours, modes, vacuum speed, questions for sensors. Any phrase can be
  tried out — a Station runs it as if you had said it out loud.
- **Room commands.** Every room title has a button of its own: what to say about the light in that
  room and in the whole home, which lamps answer "turn on the light" and which come on by name
  only.
- **Scenarios.** The scenarios from the Yandex app are listed with the phrases that start them, and
  with the same test button.

### Working with Home Assistant

- **Expose an entity to Alice, and take it away again.** Finds the entities in Home Assistant that
  Alice does not have yet, adds a label and asks Yandex to refresh the list. **Remove from Alice**
  (Убрать из Алисы) takes the label off and deletes the device; the entity itself stays in
  Home Assistant.
- **Delete a device from the Yandex home.** Devices that did not come from Home Assistant have a
  **Delete** button (Удалить) at the bottom of the card, which removes the device from the Yandex
  home altogether. The panel asks for confirmation, but it cannot bring a deleted device back.
- **Refresh the list** (Обновить список). Asks Yandex to go through the Home Assistant skill
  again — freshly exposed entities show up in Alice after that. Until at least one device has been
  exposed from Home Assistant, there is no skill and nothing to refresh — expose one
  entity to Alice first.

### Safety net

- **Name snapshot.** If Yandex recreates a device, its synonyms and its role are gone. The panel
  keeps the last good set and offers to put it back with one button — in the device card the
  section is called simply **Snapshot** (Слепок). It writes the snapshots itself, but only for
  devices with a Home Assistant entity behind them: every time it reads the list, and straight
  away after you change something from the panel. Yandex's own devices are not covered.
- **The blink check.** Lights, sockets and switches have a button that turns the device on for
  three seconds and off again — handy when a room has three identical lamps and you cannot tell
  which is which. Curtains, kettles and sensors have no such button.

### When there is more than one account or home

- **Several Yandex accounts.** If Home Assistant has more than one, the integration options let you
  pick which account the panel works with.
- **Several homes.** If the account has more than one home (a flat and a country house), each gets
  a tab of its own: its own rooms, scenarios and Stations for testing phrases.

## Before you install

| Requirement | Why |
|---|---|
| Home Assistant 2024.8 or newer | Uses the current way of registering a panel |
| [Yandex Station](https://github.com/AlexxIT/YandexStation) (AlexxIT) | **Required.** This is where access to the Yandex home comes from: it keeps cookies and tokens fresh by itself |
| [Yandex Smart Home](https://github.com/dext0r/yandex_smart_home) (dext0r) | Needed to expose Home Assistant entities to Alice. Without it the panel still shows and edits your devices, but there is nothing to add |

If you use Yandex Smart Home and want to add devices straight from the panel, the Yandex Smart
Home entity filter has to be set to **label** mode — the label is exactly what the panel puts on
and takes off.

## Installation

### Through HACS

1. HACS → the three dots in the top right corner → **Custom repositories**.
2. URL `https://github.com/busyava/yandex-menu-for-home-assistant`, category **Integration**.
3. Find **Yandex Menu for Home Assistant** in the list — in HACS the name is English — and click
   **Download**.
4. Restart Home Assistant.
5. **Settings → Devices & services → Add integration → Яндекс меню.** The name is in Russian here,
   but it is the same integration. No login and no password are asked for, only a confirmation.
   And if Home Assistant has several Yandex Station or Yandex Smart Home entries, the form asks
   which one to work with.

### By hand

1. Copy the `custom_components/yandex_menu` folder into `/config/custom_components/` on your
   Home Assistant.
2. Restart Home Assistant.
3. Add the integration the same way as above.

After that a **Яндекс меню** item appears in the sidebar. Only administrators see it. If it is not
there, reload the page with Ctrl+Shift+R — browsers cache the sidebar.

The item can be taken out of the sidebar: **Settings → Devices & services → Яндекс меню →
Configure**. The panel itself stays available at `/yandex-menu`.

## How to use it

On the left there is the list of devices by room: the name, the linked Home Assistant entity, the
synonyms and the role. A device that is switched on has its icon highlighted. Clicking a device
opens its card on the right. On a phone the system back button closes the card as well: the first
press closes the card, the second takes you off the panel (and if you opened the device from a room
card, back takes you there first).

Yandex takes its time with the list: a home of thirty-odd devices needs about ten seconds. So the
panel opens with the list it read last time and fetches a fresh one by itself. While that is going
on, an icon spins in the header next to the title, and then the list on screen quietly updates. If
the refresh fails, the icon turns yellow and the previous list stays on screen, fully usable.
Pressing the yellow icon tries again.

### Names

The first name in the list is the primary one, and it is the one the Yandex app shows. The rest
work as equal synonyms: you can say "turn on the night light" or "turn on the chandelier ambient
light" once both names are there.

To move a synonym up to primary, click the star. Yandex has no "rename" command: names can only be
added and removed, and the primary one is whichever was added first. So the panel does it for you —
it takes the other names off and puts them back after the one you picked.

Five names is the limit. Yandex turns down the sixth, so the panel greys the field out before you
get there.

### The light role

"Alice, turn on the light" switches on only the lamps in the room whose role is **main light**
(Основной свет). Anything marked **secondary** (Дополнительный) comes on by name, or with "turn on
the ambient light". The role switch sits in the lamp's card — on the lamps where Yandex allows the
role to be changed at all. On the others it is fixed, and the card has no **Room role**
(Роль в комнате) section at all.

### What to say to Alice

The icons at the right-hand end of a device row show what it can do: on and off, brightness,
colour, modes, sensor readings. Clicking them opens the card straight at **What to say to Alice**
(Что сказать Алисе), with the words for each of those. Long lists, colours for instance, start out
collapsed.

![The "What to say to Alice" section in a device card: what the device can do and the words for commands](https://raw.githubusercontent.com/busyava/yandex-menu-for-home-assistant/main/docs/say.png)

Click a word to pick it, and ▶ to test it. The panel shows the whole phrase — you can edit it
first, for example to put the device name into the right grammatical case — and a Station then runs
it for real. By default it takes the Station in the same room, and it remembers your choice.

Only what Yandex itself knows can be done by voice: it has its own set of colours and light modes.
If a light strip has a hundred effects, Alice can control only the ones Yandex Smart Home maps
onto Yandex modes.

### Room commands and scenarios

The **commands** button (команды) next to a room title opens the light commands for that room and
for the whole home. It also shows which lamps answer "Alice, turn on the light" and which come on
by name only.

Below the device list there is a **Scenarios** block (Сценарии): the scenarios from the Yandex app
with the phrases that start them and the same test button.

![Room commands and the list of Yandex scenarios with their trigger phrases](https://raw.githubusercontent.com/busyava/yandex-menu-for-home-assistant/main/docs/room.png)

### Exposing a device to Alice

Start typing a name or an entity ID into the search box, and an **In Home Assistant, but not
exposed to Alice** (Есть в Home Assistant, но не отдано в Алису) section appears. **Expose to
Alice** (Отдать в Алису) puts the label on and asks Yandex to refresh the list; the device turns up
within a minute.

![The "In Home Assistant, but not exposed to Alice" section: Home Assistant entities Alice does not have yet](https://raw.githubusercontent.com/busyava/yandex-menu-for-home-assistant/main/docs/expose.png)

Yandex will not take an entity that is `unavailable` or `unknown` — the panel warns you about that
and puts the label on anyway, so the device appears once the entity comes back to life and you
press **Refresh the list** (Обновить список).

If you have several homes, this section is only visible in the home that already holds devices from
Home Assistant.

## Good to know

The integration works through the same private API the Yandex app uses. It has no official
documentation, and Yandex can change it without warning — the panel will then need fixing. Almost
everything it does can be done by hand in the app just as well. There is one exception — the
**Delete** button (Удалить) in a device card: it removes the device from the Yandex home, the panel
cannot bring it back, and that is why it asks for confirmation first.

The panel is not meant for controlling devices day to day — Home Assistant has ordinary cards for
that. The ▶ button is there to test a phrase, not to replace a switch.

If Home Assistant has several Yandex accounts (several Yandex Station entries) or several
Yandex Smart Home entries, pick the right ones during setup or later: **Settings → Devices &
services → Яндекс меню → Configure**. Until you choose, the panel takes the first account. The
current account is shown in the panel header when there is more than one.

If the account has several homes, tabs appear in the panel header. The main home opens first; after
that the panel remembers your last choice. Each home shows its own rooms, scenarios and Stations
(a scenario tied to no home at all shows up in every home at once): a phrase is tested by a Station
in the same home, and name clashes are looked for inside one home only, because that is the only
place Alice confuses them. If a search finds something in another home, a link to it appears
above the list. That hint counts devices only: scenarios in other homes go unnoticed.

Exposing Home Assistant entities to Alice, though, works in one home only — the one where such
devices already are, or the main one if there are none anywhere yet. In the other homes the
**In Home Assistant, but not exposed to Alice** (Есть в Home Assistant, но не отдано в Алису)
section does not work: in its place, at the bottom of the list, there is an **Expose to Alice**
(Отдать в Алису) block with a hint about which home to go to for it — and it is visible without
a search too.

## What goes out, and where

The integration reaches out to one place only — the Yandex cloud at `iot.quasar.yandex.ru`, the
same one the Yandex app talks to. There are no other addresses in the code, the integration
installs no third-party libraries, and it sends no statistics about you anywhere.

The panel has no Yandex login of its own: requests ride on the Yandex Station session, and it is
Yandex Station that holds the cookies and tokens. The panel never sees your password; from the
account it takes the login the Yandex Station entry is registered under, and that is what the
snapshots are filed under. The panel header, when there is more than one account, shows something
else — the name of the Yandex Station entry itself, usually the same login. Remove Yandex Station
and the panel simply stops working.

What goes to Yandex is exactly what you would change by hand in the app: for reading — the list of
devices, rooms and scenarios; for writing — names, the room, the light role, the blink check, the
request to refresh the list and the deletion of a device. The phrase you test with ▶ is run by your
own Station: the command goes to it through the Yandex Station integration, and no separate
connection appears for that.

The panel page in the browser makes no outside calls at all — it talks only to your Home Assistant
over its usual connection, and it is the server that goes to Yandex. In the browser itself it
remembers two small things: which home is open and which Station is picked for testing phrases (the
keys `yandex_menu.house` and `yandex_menu.station`). Those entries stay in the browser and go
nowhere.

The integration keeps two files on disk in Home Assistant.
`config/.storage/yandex_menu.snapshots` holds the snapshots: a device's names, its room and its
light role. They are there so you can put the settings back if Yandex recreates a device — the
button puts back the names and the role, and leaves the room as it is.
`config/.storage/yandex_menu.list` holds the last list read: the same thing the panel shows on
screen, kept so that it opens at once next time. There are no passwords or tokens in it. The
integration deletes this file itself when it is removed.

The panel and all its commands are open to Home Assistant administrators only: an ordinary user
sees neither the sidebar item nor the data.

## How to remove it

**Settings → Devices & services → Яндекс меню → Delete.** The sidebar item disappears at once. If
you installed through HACS, delete the **Yandex Menu for Home Assistant** repository there as well;
if you installed by hand, delete the `custom_components/yandex_menu` folder. After a restart of
Home Assistant nothing of the integration is left running.

A few things stay behind, and that is normal:

- **Devices and names in the Yandex home.** The panel changed them in the Yandex cloud, not on your
  own system, so everything stays as it is — just as it would if you had changed it in the app.
- **Labels on entities** that the panel added with **Expose to Alice** (Отдать в Алису). They are
  not junk: the label is how Yandex Smart Home decides what to hand over to Alice, and without it
  the device disappears from Alice. If a device really is not needed any more, take it away in
  advance with **Remove from Alice** (Убрать из Алисы) — that removes the label and deletes the
  device at Yandex. Any labels left over can be edited where Home Assistant keeps all of
  them — in its settings, in the section with areas and labels.
- **The snapshot file** `config/.storage/yandex_menu.snapshots` — a few kilobytes of text. Delete
  it or leave it: if you bring the integration back, the snapshots come in useful again.

## If something goes wrong

**No sidebar item.** Reload the page with Ctrl+Shift+R.

**«Не найдена интеграция Яндекс.Станция»** (the Yandex Station integration was not found). Set
[Yandex Station](https://github.com/AlexxIT/YandexStation) up first; that is where access to the
Yandex home comes from.

**The header icon turned yellow.** The list did not refresh, and the previous one is on screen.
What Yandex answered is in the icon's tooltip, and on a phone it shows up when you tap the icon.
The tap also tries again. If there is no previous list, Yandex's answer is written right where the
list would be, and the icon is there to try again.

**The device did not appear after Expose to Alice (Отдать в Алису).** Most often the entity is
`unavailable` or `unknown`, and Yandex does not take those. Bring it back to life and press
**Refresh the list** (Обновить список).

**A device turned up named "0".** That comes from an empty alias in the Home Assistant entity
registry. The panel clears aliases before exposing an entity, but if the device was created
earlier, delete it in the panel and expose the entity again.

**«Аккаунт Яндекса, выбранный в настройках, больше не подключён.»** (the Yandex account chosen in
the options is no longer connected). It was removed from Yandex Station; pick another one in the
integration options.

**An error right in the panel.** The panel shows what Yandex answers as it is, rewriting nothing.
Its own checks are shown the same way — when you type a name, for instance: «Такое имя у устройства
уже есть.» (this device already has that name), and once five names have piled up — «Занято 5 имён
из 5 — это потолок Яндекса.» (5 names out of 5 taken — that is Yandex's limit).

If none of this helped, describe the problem in
[Issues](https://github.com/busyava/yandex-menu-for-home-assistant/issues). Three things help: the
Home Assistant version, the plugin version and the lines from the log — **Settings → System →
Logs**, search for `yandex_menu`.

## Support the project

The plugin is free and will stay that way. If it came in handy, you can buy the author a coffee:

[![Buy the author a coffee](https://raw.githubusercontent.com/busyava/yandex-menu-for-home-assistant/main/docs/coffee-en.png)](https://pay.cloudtips.ru/p/a2eedc67)

If the image did not load, here is the direct link: https://pay.cloudtips.ru/p/a2eedc67

You choose the amount, payment is by card, no sign-up needed. Cards issued by Russian banks only.

## License

MIT — see [LICENSE](LICENSE).
