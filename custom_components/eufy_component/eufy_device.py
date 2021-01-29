from .const import DOMAIN, SUBSCRIBE_PROPERTY, DEVICE_STATE
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC

from eufySecurityApi.const import PARAM_TYPE
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity
)

import logging

_LOGGER = logging.getLogger(__name__)
class BaseDevice(CoordinatorEntity, Entity):

    def __init__(self, api, device, coordinator):
        super().__init__(coordinator)
        self._api = api
        self._device = device
        self._device.subscribe(SUBSCRIBE_PROPERTY, self.async_update_callback)

    @property
    def device_info(self):
        """Return a device description for device registry."""
        parentStation = self._device.api.stations[self._device.station_sn]
        return {
            "connections": {(CONNECTION_NETWORK_MAC, self._device.wifi_mac)},
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._device.serial)
            },
            "manufacturer": 'Eufy',
            "model": self._device.model,
            "name": self._device.name,
            "sw_version": self._device.main_sw_version,
            "via_device": (CONNECTION_NETWORK_MAC, parentStation.wifi_mac)
        }

    
    @callback
    def async_update_callback(self, attributes):
        _LOGGER.info('api call homeassistant for update')
        self.async_write_ha_state()

    @property
    def available(self):
        """Return True if device is available."""
        return self._device.status == DEVICE_STATE.ONLINE
        # return self._device.status in [
        #     DEVICE_STATE.ONLINE
        # ]

    @property
    def name(self):
        """Return the name of the device."""
        return self._device.name

    @property
    def unique_id(self):
        return self._device.serial + '_' + self.device_class.replace(' ', '_').lower()