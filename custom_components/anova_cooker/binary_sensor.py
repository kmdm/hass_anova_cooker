from typing import Optional

from aionova import AnovaCookerLegacy
from homeassistant.components.binary_sensor import BinarySensorEntity, DEVICE_CLASS_PROBLEM
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    cooker, coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([
        AnovaCookerAlarmBinarySensor(coordinator, cooker),
    ], True)


class AnovaCookerAlarmBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator: DataUpdateCoordinator, cooker: AnovaCookerLegacy):
        super().__init__(coordinator)
        self.cooker = cooker

    @property
    def name(self) -> Optional[str]:
        return f'{self.cooker.cooker_id} alarm'

    @property
    def unique_id(self) -> Optional[str]:
        return f'{self.cooker.cooker_id}_alarm'

    @property
    def is_on(self):
        return False if 'off' == self.cooker.mode else self.cooker.alarm_active

    @property
    def icon(self) -> Optional[str]:
        return 'mdi:alarm' if self.is_on else 'mdi:alarm-off'

