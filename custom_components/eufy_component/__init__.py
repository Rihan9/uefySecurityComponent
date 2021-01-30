from datetime import timedelta

from homeassistant import core
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import SOURCE_REAUTH, ConfigEntry
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from eufySecurityApi.api import Api
from eufySecurityApi.const import PARAM_TYPE
from .const import EUFY_TOKEN, EUFY_TOKEN_EXPIRE_AT, EUFY_DOMAIN, DOMAIN, ENTITY_TYPE_BATTERY, ENTITY_TYPE_MOTION_SENSOR, HASS_EUFY_API, USED_ENTITIES_DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the Eufy Component component."""
    # @TODO: Add exception code.
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    _LOGGER.info('config entry unique id: %s' % entry.unique_id)
    # if entry.unique_id is None and entry.data['unique_id'] is not None:
    #     new_data = dict(entry.data)
    #     hass.config_entries.async_update_entry(
    #         entry, unique_id=entry.data['unique_id'][:10], data=new_data
    #     )
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    
    EufyApi = Api(
        token=entry.data.get(EUFY_TOKEN), 
        token_expire_at=entry.data.get(EUFY_TOKEN_EXPIRE_AT), 
        domain=entry.data.get(EUFY_DOMAIN)
    )
    # await EufyApi.update()
    if(not EufyApi.connected):
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": SOURCE_REAUTH},
                data=entry.data,
            )
        )
        return False
    
    _LOGGER.info('setting up coordinator...')
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name="EufyApi",
        update_method=EufyApi.update,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta(seconds=2),
    )
    
    hass.data[DOMAIN][entry.unique_id] = {
        'Api': EufyApi,
        'coordinator': coordinator
    }

    await coordinator.async_refresh()

    
    _LOGGER.info('setting up devices and entities...')

    device_registry = await dr.async_get_registry(hass)
    for station_sn in EufyApi.stations:
        station = EufyApi.stations[station_sn]
        device_registry.async_get_or_create(
            identifiers={(DOMAIN, station_sn)},
            manufacturer="Eufy",
            name=station.name,
            model=station.model,
            sw_version=station.main_sw_version,
            config_entry_id=entry.unique_id,
            connections={(CONNECTION_NETWORK_MAC, station.wifi_mac)},
        )
    
    for entity_domain in USED_ENTITIES_DOMAIN:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(
                entry, entity_domain
            )
        )
    return True


async def async_unload_entry(hass, entry):
    for entity_domain in USED_ENTITIES_DOMAIN:
        await hass.config_entries.async_forward_entry_unload(entry, entity_domain)

    device_registry = await dr.async_get_registry(hass)
    for hass_device in dr.async_entries_for_config_entry(device_registry, entry.unique_id):
        device_registry.async_remove_device(hass_device.id)
    hass.data[DOMAIN] = {}

    return True
    
