from aionova import AnovaCookerLegacy
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from typing import Optional, Any

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: callable):
    cooker, coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([
        AnovaCookerSpeakerSwitch(coordinator, cooker),
    ], True)


class AnovaCookerSpeakerSwitch(CoordinatorEntity, SwitchEntity):
    def __init__(self, coordinator: DataUpdateCoordinator, cooker: AnovaCookerLegacy):
        super().__init__(coordinator)
        self.cooker = cooker

    @property
    def is_on(self) -> bool:
        return self.cooker.speaker_mode

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.cooker.set_speaker_mode(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.cooker.set_speaker_mode(False)
        await self.coordinator.async_request_refresh()

    @property
    def name(self) -> Optional[str]:
        return f'{self.cooker.cooker_id} speaker enabled'

    @property
    def unique_id(self) -> Optional[str]:
        return f'{self.cooker.cooker_id}_speaker_enabled'

    @property
    def icon(self) -> Optional[str]:
        return 'mdi:volume-medium' if self.is_on else 'mdi:volume-off'
