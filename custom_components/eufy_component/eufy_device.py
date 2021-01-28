from .const import DOMAIN, SUBSCRIBE_PROPERTY, DEVICE_STATE
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity

class BaseDevice(Entity):

    def __init__(self, api, device):
        self._api = api
        self._device = device

    @property
    def device_info(self):
        """Return a device description for device registry."""

        return {
            "connections": self._device.station_sn,
            "identifiers": self._device.serial,
            "manufacturer": 'Eufy',
            "model": self._device.model,
            "name": self._device.name,
            "sw_version": self._device.PROP_MAIN_SW_VERSION,
            "via_device": (DOMAIN, self._device.station_sn),
        }

    async def async_added_to_hass(self):
        self._device.subscribe(SUBSCRIBE_PROPERTY, self.async_update_callback)

    
    @callback
    def async_update_callback(self, attributes):
        self.async_write_ha_state()

    @property
    def available(self):
        """Return True if device is available."""
        return self._device.state in [
            DEVICE_STATE.ONLINE
        ]

    @property
    def name(self):
        """Return the name of the device."""
        return self._device.name

    @property
    def should_poll(self):
        """No polling needed."""
        return False