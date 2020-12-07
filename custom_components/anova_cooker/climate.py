from aionova import AnovaCookerLegacy
from homeassistant.components.climate import ClimateEntity, HVAC_MODE_HEAT, HVAC_MODE_OFF
from homeassistant.components.climate.const import CURRENT_HVAC_OFF, CURRENT_HVAC_HEAT, SUPPORT_TARGET_TEMPERATURE, \
    CURRENT_HVAC_IDLE
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS, TEMP_FAHRENHEIT, ATTR_TEMPERATURE
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.util.temperature import convert as convert_temperature

from typing import Optional, Dict, List

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: callable):
    cooker, coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async def handle_stop_alarm(entity, service_call):
        await entity.cooker.stop_alarm()
        await entity.coordinator.async_request_refresh()

    platform = entity_platform.current_platform.get()
    platform.async_register_entity_service(
        'stop_alarm',
        {},
        handle_stop_alarm
    )

    async_add_entities([
        AnovaCookerClimateDevice(coordinator, cooker),
    ], True)


class AnovaCookerClimateDevice(CoordinatorEntity, ClimateEntity):
    def __init__(self, coordinator: DataUpdateCoordinator, cooker: AnovaCookerLegacy):
        super().__init__(coordinator)
        self.cooker = cooker

    @property
    def name(self) -> Optional[str]:
        return f'{self.cooker.cooker_id} cooker'

    @property
    def unique_id(self) -> Optional[str]:
        return f'{self.cooker.cooker_id}_cooker'

    @property
    def current_temperature(self) -> Optional[float]:
        return float(self.cooker.current_temperature)

    @property
    def target_temperature(self) -> Optional[float]:
        return float(self.cooker.target_temperature)

    @property
    def temperature_unit(self) -> str:
        return TEMP_CELSIUS if 'c' == self.cooker.temperature_unit else TEMP_FAHRENHEIT

    @property
    def hvac_modes(self) -> List[str]:
        return [HVAC_MODE_OFF, HVAC_MODE_HEAT]

    @property
    def hvac_mode(self) -> str:
        if 'off' == self.cooker.mode:
            return HVAC_MODE_OFF

        return HVAC_MODE_HEAT

    @property
    def hvac_action(self) -> Optional[str]:
        if 'off' == self.cooker.mode:
            return CURRENT_HVAC_OFF
        elif 'maintaining' == self.cooker.mode:
            return CURRENT_HVAC_IDLE

        return CURRENT_HVAC_HEAT
    
    @property
    def supported_features(self) -> int:
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def min_temp(self) -> float:
        return convert_temperature(0, TEMP_CELSIUS, self.temperature_unit)

    @property
    def max_temp(self) -> float:
        return convert_temperature(100, TEMP_CELSIUS, self.temperature_unit)

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        if HVAC_MODE_OFF == hvac_mode:
            await self.cooker.stop_job()
        elif HVAC_MODE_HEAT == hvac_mode:
            await self.cooker.start_job()
        else:
            raise NotImplementedError

        await self.coordinator.async_request_refresh()

    async def async_set_temperature(self, **kwargs) -> None:
        await self.cooker.set_target_temperature(kwargs.get(ATTR_TEMPERATURE))
        await self.coordinator.async_request_refresh()

