from .const import HASS_EUFY_API, DOMAIN, ENTITY_TYPE_MOTION_SENSOR, PARAM_TYPE_TO_ENTITIES, PARAM_TYPE
from .eufy_device import BaseDevice
from .utils import wrap
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
        if(device.isDoorSensor):
            entities.append(
                DoorSensor(EufyApi, device, coordinator)
            )
        entities += make_sensor_from_attribute(EufyApi, device, coordinator)
    for station_sn in EufyApi.stations:
        station = EufyApi.stations[station_sn]
        entities += make_sensor_from_attribute(EufyApi, station, coordinator)
    if(len(entities) > 0):
        async_add_devices(entities)  
    
def make_sensor_from_attribute(api, device, coordinator):
    entities = []
    for attribute in device.attribute:
        if attribute in PARAM_TYPE_TO_ENTITIES:
            p_domain, p_name, p_icon = PARAM_TYPE_TO_ENTITIES[attribute]
            if(p_domain != 'binary_sensor'):
                continue
            entities.append(
                AttributeBinarySensor(
                    api, device, coordinator, attribute, p_name % device.name, p_icon
                )
            )
    return entities


async def async_remove_entry(hass, entry) -> None:
    EufyApi = hass.data[DOMAIN][entry.unique_id]['Api']

    entity_registry = await er.async_get_registry(hass)
    for device_sn in EufyApi.devices:
        device = EufyApi.devices[device_sn]
        if(device.isMotionSensor):
            entity_id = entity_registry.async_get_entity_id(DOMAIN, 'bynary_sensor', device.serial + '_' + DEVICE_CLASS_MOTION.replace(' ', '_').lower())
            if(entity_id is not None):
                entity_registry.async_remove(entity_id)
        for attribute in device.attribute:
            if(attribute in PARAM_TYPE_TO_ENTITIES):
                entity_id = entity_registry.async_get_entity_id(
                    DOMAIN, 'bynary_sensor', device.serial + '_' + attribute.name.replace(' ', '_').lower())
                if(entity_id is not None):
                    entity_registry.async_remove(entity_id)

class AttributeBinarySensor(BaseDevice):

    def __init__(self, api, device, coordinator, attribute, name, icon='mdi:menu'):
        super().__init__(api, device, coordinator)
        self._attribute = attribute
        self._icon = icon
        self._name = name
    
    @property
    def name(self):
        return self._name
    
    @property
    def unique_id(self):
        return self._device.serial + '_' + self._attribute.name.replace(' ', '_').lower()

    @property
    def icon(self):
        return self._icon

    
    @property
    def device_class(self):
        return None

    
    @property
    def is_on(self):
        return wrap(
            self._device,
            self._attribute
        )
    
    @property
    def state(self):
        """Return the state of the binary sensor."""
        return STATE_ON if self.is_on else STATE_OFF


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


class MotionSensor(BaseDevice):

    @property
    def is_on(self):
        return wrap(
            self._device,
            PARAM_TYPE.SENSOR_CONTACT_OPEN
        ) == '1'
    
    @property
    def device_class(self):
        return DEVICE_CLASS_MOTION

    @property
    def state(self):
        """Return the state of the binary sensor."""
        return STATE_ON if self.is_on else STATE_OFF
    