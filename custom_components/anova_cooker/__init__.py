"""The ANOVA Precision Cooker integration."""
from datetime import timedelta
from typing import Optional

import aionova
import asyncio
import async_timeout
import functools
import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN
from ...helpers.update_coordinator import DataUpdateCoordinator, T

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

PLATFORMS = ["binary_sensor", "climate", "sensor", "switch"]

_LOGGER = logging.getLogger(__name__)


class AnovaDataUpdateCoordinator(DataUpdateCoordinator):
    update_failed_count = 0

    @callback
    def _schedule_refresh(self) -> None:
        if not self.last_update_success:
            self.update_failed_count += 1
        else:
            self.update_failed_count = 0

        self.update_interval = timedelta(seconds=15 if self.update_failed_count < 3 else 300)
        super()._schedule_refresh()


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the ANOVA Precision Cooker component."""
    hass.data[DOMAIN] = {}

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up ANOVA Precision Cooker from a config entry."""

    cooker = aionova.AnovaCookerLegacy(entry.data['cooker_id'], entry.data['cooker_secret'])

    async def async_update_data():
        async with async_timeout.timeout(10):
            await cooker.update_state()
            return cooker.state

    coordinator = AnovaDataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f'{entry.data["cooker_id"]} updater',
        update_method=async_update_data,
        update_interval=timedelta(seconds=15)
    )

    await coordinator.async_refresh()

    hass.data[DOMAIN][entry.entry_id] = (cooker, coordinator)

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
