from homeassistant import core
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from eufySecurityApi.api import Api
from .const import TOKEN, TOKEN_EXPIRE_AT, DOMAIN

import logging

_LOGGER = logging.getLogger(__name__)

# async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
#     """Set up the Eufy Component component."""
#     # @TODO: Add exception code.
#     return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    EufyApi = Api(token=entry.get(TOKEN), token_expire_at=entry.get(TOKEN_EXPIRE_AT), domain=entry.get(DOMAIN))
    EufyApi.update()
    for device_sn in EufyApi.devices:
        _LOGGER.info('device_sn: %s, name: %s' % (device_sn, EufyApi.devices.get(device_sn).name))