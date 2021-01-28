from .const import HASS_EUFY_API, DOMAIN, ENTITY_TYPE_BATTERY
from .eufy_device import BaseDevice

from homeassistant.const import (
    DEVICE_CLASS_BATTERY,
    PERCENTAGE
)
async def async_setup_entry(hass, config_entry, async_add_devices):
    
    """Set up the sensor platform."""
    EufyApi = hass.config[DOMAIN][HASS_EUFY_API]
    typeMap = {
        ENTITY_TYPE_BATTERY: BatterySensor
    }
    await async_add_devices([
        typeMap[config_entry['type']](EufyApi, EufyApi.devices[config_entry['sn']])
    ])
    """Set up entry."""
def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    EufyApi = hass.config[DOMAIN][HASS_EUFY_API]
    typeMap = {
        ENTITY_TYPE_BATTERY: BatterySensor
    }
    add_entities([
        typeMap[config['type']](EufyApi, EufyApi.devices[config['sn']])
    ])


class BatterySensor(BaseDevice):

    @property
    def state(self):
        self._device.battery_level
    
    @property
    def unit_of_measurement(self):
        return PERCENTAGE
    
    @property
    def device_class(self):
        return DEVICE_CLASS_BATTERY
    
