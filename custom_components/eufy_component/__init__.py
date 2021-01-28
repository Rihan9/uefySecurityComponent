from homeassistant import core
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr
from eufySecurityApi.api import Api
from .const import EUFY_TOKEN, EUFY_TOKEN_EXPIRE_AT, EUFY_DOMAIN, DOMAIN

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the Eufy Component component."""
    # @TODO: Add exception code.
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    entry.data
    EufyApi = Api(
        token=entry.data.get(EUFY_TOKEN), 
        token_expire_at=entry.data.get(EUFY_TOKEN_EXPIRE_AT), 
        domain=entry.data.get(EUFY_DOMAIN)
    )
    await EufyApi.update()
    device_registry = await dr.async_get_registry(hass)
    for station_sn in EufyApi.stations:
        station = EufyApi.stations[station_sn]
        device_registry.async_get_or_create(
            config_entry_id=station_sn,
            identifiers={(DOMAIN, station_sn)},
            manufacturer="Eufy",
            name=station.name,
            model=station.model,
            sw_version=station.PROP_MAIN_SW_VERSION,
        )
    for device_sn in EufyApi.devices:
        _LOGGER.info('device_sn: %s, name: %s' % (device_sn, EufyApi.devices.get(device_sn).name))
        #if EufyApi.devices[device_sn].hasBattery:


    return True