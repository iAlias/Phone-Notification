from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.storage import Store

from .const import (
    DOMAIN,
    STORAGE_KEY,
    CONF_SENSOR,
    CONF_NAME,
    CONF_MAX_HISTORY,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    entity_id = config.get(CONF_SENSOR)
    name = config.get(CONF_NAME, "Phone Notifications")
    max_history = config.get(CONF_MAX_HISTORY, 1000)

    if not entity_id:
        _LOGGER.error("È necessario specificare 'sensor_entity_id'")
        return

    sensor = PhoneNotificationsSensor(hass, name, entity_id, max_history)
    async_add_entities([sensor])


class PhoneNotificationsSensor(Entity):
    def __init__(self, hass, name: str, entity_id: str, max_history: int) -> None:
        self.hass = hass
        self._name = name
        self._source_entity = entity_id
        self._max_history = max_history
        self._store = Store(hass, 1, STORAGE_KEY.format(entity_id.replace(".", "_")))
        self._notifications: list[dict[str, Any]] = []
        self._state: str | None = None
        self._attr_icon = "mdi:cellphone-text"

        hass.loop.create_task(self._async_load())
        async_track_state_change_event(hass, [entity_id], self._state_changed)

    async def _async_load(self) -> None:
        saved = await self._store.async_load()
        if saved:
            self._notifications = saved.get("notifications", [])

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self) -> str | None:
        return self._state

    @property
    def extra_state_attributes(self):
        return {
            "history_count": len(self._notifications),
            "last_notification": self._notifications[-1] if self._notifications else None,
            "notifications": self._notifications,
        }

    @callback
    async def _state_changed(self, event) -> None:
        new_state = event.data.get("new_state")
        if new_state is None:
            return

        attrs = new_state.attributes or {}
        title = attrs.get("android.title")
        text = attrs.get("android.text")

        if not title and not text:
            return

        notification = {
            "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
            "title": title,
            "text": text,
        }

        self._state = title or text or "Notifica"
        self._notifications.append(notification)

        if len(self._notifications) > self._max_history:
            self._notifications = self._notifications[-self._max_history :]

        self.async_write_ha_state()
        await self._store.async_save({"notifications": self._notifications})