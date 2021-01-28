from .const import HASS_EUFY_API, DOMAIN, ENTITY_TYPE_MOTION_SENSOR
from .eufy_device import BaseDevice

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_MOTION
)
async def async_setup_entry(hass, config_entry, async_add_devices):
    
    """Set up the sensor platform."""
    EufyApi = hass.config[DOMAIN][HASS_EUFY_API]
    typeMap = {
        ENTITY_TYPE_MOTION_SENSOR: MotionSensor
    }
    await async_add_devices([
        typeMap[config_entry['type']](EufyApi, EufyApi.devices[config_entry['sn']])
    ])
    """Set up entry."""

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    EufyApi = hass.config[DOMAIN][HASS_EUFY_API]
    typeMap = {
        ENTITY_TYPE_MOTION_SENSOR: MotionSensor
    }
    add_entities([
        typeMap[config['type']](EufyApi, EufyApi.devices[config['sn']])
    ])


class MotionSensor(BaseDevice):

    @property
    def is_on(self):
        self._device.state == 'motion detected'
    
    @property
    def device_class(self):
        return DEVICE_CLASS_MOTION