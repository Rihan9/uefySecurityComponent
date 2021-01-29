from .const import HASS_EUFY_API, DOMAIN, ENTITY_TYPE_BATTERY
from .eufy_device import BaseDevice
import logging
from homeassistant.const import (
    DEVICE_CLASS_BATTERY,
    PERCENTAGE
)

_LOGGER = logging.getLogger(__name__)
async def async_setup_entry(hass, config_entry, async_add_devices):
    
    """Set up the sensor platform."""
    EufyApi = hass.data[DOMAIN][HASS_EUFY_API]
    for device_sn in EufyApi.devices:
        device = EufyApi.devices[device_sn]
        if(device.hasbattery):
            await async_add_devices([
                BatterySensor(EufyApi, device, config_entry.unique_id)
            ])
    """Set up entry."""

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
    
    
