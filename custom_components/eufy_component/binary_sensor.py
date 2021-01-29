from .const import HASS_EUFY_API, DOMAIN, ENTITY_TYPE_MOTION_SENSOR
from .eufy_device import BaseDevice
import logging

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_MOTION
)

_LOGGER = logging.getLogger(__name__)
async def async_setup_entry(hass, config_entry, async_add_devices):
    
    """Set up the sensor platform."""
    EufyApi = hass.data[DOMAIN][config_entry.unique_id]['Api']
    coordinator = hass.data[DOMAIN][config_entry.unique_id]['coordinator']
    entities = []
    for device_sn in EufyApi.devices:
        device = EufyApi.devices[device_sn]
        if(device.isMotionSensor):
            entities.append(
                MotionSensor(EufyApi, device, coordinator)
            )
    if(len(entities) > 0):
        async_add_devices(entities)  

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
        typeMap[discovery_info['type']](EufyApi, EufyApi.devices[discovery_info['sn']], discovery_info['config_entry_id'])
    ])


class MotionSensor(BaseDevice):

    @property
    def is_on(self):
        return self._device.motionDetected
    
    @property
    def device_class(self):
        return DEVICE_CLASS_MOTION
    