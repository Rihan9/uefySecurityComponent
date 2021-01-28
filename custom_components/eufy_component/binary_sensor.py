from .const import HASS_EUFY_API, DOMAIN, ENTITY_TYPE_MOTION_SENSOR
from .eufy_device import BaseDevice
import logging

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_MOTION
)

_LOGGER = logging.getLogger(__name__)
async def async_setup_entry(hass, config_entry, async_add_devices):
    
    """Set up the sensor platform."""
    EufyApi = hass.data[DOMAIN][HASS_EUFY_API]
    typeMap = {
        ENTITY_TYPE_MOTION_SENSOR: MotionSensor
    }
    await async_add_devices([
        typeMap[config_entry['type']](EufyApi, EufyApi.devices[config_entry['sn']])
    ])
    """Set up entry."""

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    EufyApi = hass.data[DOMAIN][HASS_EUFY_API]
    _LOGGER.debug('config: %s' % config )
    _LOGGER.debug('discovery_info: %s' % discovery_info )
    _LOGGER.debug('EufyApi: %s' % EufyApi )
    typeMap = {
        ENTITY_TYPE_MOTION_SENSOR: MotionSensor
    }
    add_entities([
        typeMap[discovery_info['type']](EufyApi, EufyApi.devices[discovery_info['sn']])
    ])


class MotionSensor(BaseDevice):

    @property
    def is_on(self):
        self._device.state == 'motion detected'
    
    @property
    def device_class(self):
        return DEVICE_CLASS_MOTION