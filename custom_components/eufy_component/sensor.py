from .const import HASS_EUFY_API, DOMAIN, ENTITY_TYPE_BATTERY, PARAM_TYPE_TO_ENTITIES, PARAM_TYPE, GUARD_MODE
from .eufy_device import BaseDevice
from .utils import wrap
import logging
from homeassistant.const import (
    DEVICE_CLASS_BATTERY,
    PERCENTAGE
)

from homeassistant.helpers import entity_registry as er



_LOGGER = logging.getLogger(__name__)
async def async_setup_entry(hass, config_entry, async_add_devices):
    
    """Set up the sensor platform."""
    EufyApi = hass.data[DOMAIN][config_entry.unique_id]['Api']
    coordinator = hass.data[DOMAIN][config_entry.unique_id]['coordinator']
    entities = []
    for device_sn in EufyApi.devices:
        device = EufyApi.devices[device_sn]
        if(device.hasbattery):
            entities.append(BatterySensor(EufyApi, device, coordinator))
        entities += make_sensor_from_attribute(EufyApi, device, coordinator)
    for station_sn in EufyApi.stations:
        station = EufyApi.stations[station_sn]
        entities += make_sensor_from_attribute(EufyApi, station, coordinator)
    
    if(len(entities) > 0):
        async_add_devices(entities)        
    """Set up entry."""

async def async_remove_entry(hass, entry) -> None:
    EufyApi = hass.data[DOMAIN][entry.unique_id]['Api']

    entity_registry = await er.async_get_registry(hass)
    for device_sn in EufyApi.devices:
        device = EufyApi.devices[device_sn]
        if(device.hasbattery):
            entity_id = entity_registry.async_get_entity_id(DOMAIN, 'sensor', device.serial + '_' + DEVICE_CLASS_BATTERY.replace(' ', '_').lower())
            if(entity_id is not None):
                entity_registry.async_remove(entity_id)
        for attribute in device.attribute:
            if(attribute in PARAM_TYPE_TO_ENTITIES):
                entity_id = entity_registry.async_get_entity_id(
                    DOMAIN, 'bynary_sensor', device.serial + '_' + attribute.name.replace(' ', '_').lower())
                if(entity_id is not None):
                    entity_registry.async_remove(entity_id)

async def make_sensor_from_attribute(api, device, coordinator):
    entities = []
    for attribute in device.attribute:
        if attribute in PARAM_TYPE_TO_ENTITIES and PARAM_TYPE_TO_ENTITIES[attribute][0] == 'sensor':
            entities.append(
                AttributeSensor(
                    api, device, coordinator, attribute, PARAM_TYPE_TO_ENTITIES[attribute][1], PARAM_TYPE_TO_ENTITIES[attribute][2]
                )
            )
    return entities

class AttributeSensor(BaseDevice):

    def __init__(self, api, device, coordinator, attribute, name, icon='mdi:menu'):
        super.__init__(self, api, device, coordinator)
        self._attribute = attribute
        self._icon = icon
        self._name = name
    
    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return wrap(
            self._device,
            self._attribute
        )
    
    @property
    def unit_of_measurement(self):
        return None
    
    @property
    def device_class(self):
        return None
    
    @property
    def unique_id(self):
        return self._device.serial + '_' + self._attribute.name.replace(' ', '_').lower()

    @property
    def icon(self):
        return self._icon
        

class BatterySensor(BaseDevice):

    @property
    def state(self):
        return self._device.battery_level
    
    @property
    def unit_of_measurement(self):
        return PERCENTAGE
    
    @property
    def device_class(self):
        return DEVICE_CLASS_BATTERY
    
    
