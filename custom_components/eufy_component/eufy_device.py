from .const import DOMAIN

class BaseDevice(object):
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