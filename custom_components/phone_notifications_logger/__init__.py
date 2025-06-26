"""Inizializzazione dell'integrazione Phone Notifications Logger."""

from __future__ import annotations
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Setup tramite configuration.yaml (retro‑compatibilità)."""
    return True  # Non usiamo configurazione YAML diretta qui.

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setup da Config Entry (non implementato)."""
    return True