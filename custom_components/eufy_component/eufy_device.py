from .const import DOMAIN, SUBSCRIBE_PROPERTY, DEVICE_STATE
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC

from eufySecurityApi.const import PARAM_TYPE

class BaseDevice(Entity):

    def __init__(self, api, device, config_entry_id):
        self._api = api
        self._device = device
        self._config_entry_id = config_entry_id

    @property
    def device_info(self):
        """Return a device description for device registry."""
        parentStation = self._device.api.stations[self._device.station_sn]
        return {
            "connections": {(CONNECTION_NETWORK_MAC, self._device.attribute[PARAM_TYPE.PROP_WIFI_MAC])},
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._device.serial)
            },
            "manufacturer": 'Eufy',
            "model": self._device.model,
            "name": self._device.name,
            "sw_version": self._device.attribute[PARAM_TYPE.PROP_MAIN_SW_VERSION],
            "via_device": {(CONNECTION_NETWORK_MAC, parentStation.attribute[PARAM_TYPE.PROP_WIFI_MAC])}
        }

    async def async_added_to_hass(self):
        self._device.subscribe(SUBSCRIBE_PROPERTY, self.async_update_callback)

    
    @callback
    def async_update_callback(self, attributes):
        self.async_write_ha_state()

    @property
    def available(self):
        """Return True if device is available."""
        return self._device.attribute[PARAM_TYPE.PROP_STATUS] == DEVICE_STATE.ONLINE
        # return self._device.status in [
        #     DEVICE_STATE.ONLINE
        # ]

    @property
    def name(self):
        """Return the name of the device."""
        return self._device.name

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def unique_id(self):
        return self._device.serial