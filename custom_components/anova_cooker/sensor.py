from aionova import AnovaCookerLegacy
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TIME_SECONDS, DEVICE_CLASS_TIMESTAMP
from homeassistant.core import HomeAssistant
from typing import Optional

from .const import DOMAIN
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: callable):
    cooker, coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([
        AnovaCookerTimeRemainingSensor(coordinator, cooker)
    ], True)


class AnovaCookerTimeRemainingSensor(CoordinatorEntity):
    def __init__(self, coordinator: DataUpdateCoordinator, cooker: AnovaCookerLegacy):
        super().__init__(coordinator)
        self.cooker = cooker

    @property
    def unit_of_measurement(self) -> Optional[str]:
        return TIME_SECONDS

    @property
    def state(self):
        return self.cooker.time_remaining or 0

    @property
    def name(self) -> Optional[str]:
        return f'{self.cooker.cooker_id} time remaining'

    @property
    def unique_id(self) -> Optional[str]:
        return f'{self.cooker.cooker_id}_time_remaining'

    @property
    def icon(self) -> Optional[str]:
        return 'mdi:timer'
