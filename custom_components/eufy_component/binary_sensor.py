from .const import HASS_EUFY_API, DOMAIN, ENTITY_TYPE_MOTION_SENSOR
from .eufy_device import BaseDevice
import logging

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_MOTION
)
from homeassistant.const import STATE_OFF, STATE_ON

from homeassistant.helpers import entity_registry as er

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

async def async_remove_entry(hass, entry) -> None:
    EufyApi = hass.data[DOMAIN][entry.unique_id]['Api']

    entity_registry = await er.async_get_registry(hass)
    for device_sn in EufyApi.devices:
        device = EufyApi.devices[device_sn]
        if(device.isMotionSensor):
            entity_id = entity_registry.async_get_entity_id(DOMAIN, 'bynary_sensor', device.serial + '_' + DEVICE_CLASS_MOTION.replace(' ', '_').lower())
            if(entity_id is not None):
                entity_registry.async_remove(entity_id)

class MotionSensor(BaseDevice):

    @property
    def is_on(self):
        return self._device.motionDetected
    
    @property
    def device_class(self):
        return DEVICE_CLASS_MOTION

    @property
    def state(self):
        """Return the state of the binary sensor."""
        return STATE_ON if self.is_on else STATE_OFF
    