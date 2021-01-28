from datetime import timedelta

from homeassistant import core
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from eufySecurityApi.api import Api
from .const import EUFY_TOKEN, EUFY_TOKEN_EXPIRE_AT, EUFY_DOMAIN, DOMAIN, ENTITY_TYPE_BATTERY, ENTITY_TYPE_MOTION_SENSOR, HASS_EUFY_API
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the Eufy Component component."""
    # @TODO: Add exception code.
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    if entry.unique_id is None and entry.data.unique_id is not None:
        await hass.config_entries.async_update_entry(
            entry, unique_id=entry.data.unique_id, data=entry.data
        )
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    entry.data
    EufyApi = Api(
        token=entry.data.get(EUFY_TOKEN), 
        token_expire_at=entry.data.get(EUFY_TOKEN_EXPIRE_AT), 
        domain=entry.data.get(EUFY_DOMAIN)
    )
    hass.data[DOMAIN][HASS_EUFY_API] = EufyApi
    # await EufyApi.update()
    
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

    
    hass.data[DOMAIN]['Coordinator'] = coordinator

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
            sw_version=station.PROP_MAIN_SW_VERSION,
            config_entry_id=entry.unique_id
        )
    for device_sn in EufyApi.devices:
        device = EufyApi.devices[device_sn]
        _LOGGER.info('device_sn: %s, name: %s' % (device_sn, device.name))
        # device_registry.async_get_or_create(
        #     config_entry_id=device_sn,
        #     identifiers={(DOMAIN, device_sn)},
        #     manufacturer="Eufy",
        #     name=device.name,
        #     model=device.model,
        #     sw_version=device.PROP_MAIN_SW_VERSION,
        #     config_entry_id=config_entry.unique_id
        # )
        if(EufyApi.devices[device_sn].hasbattery):
            hass.async_create_task(
                hass.helpers.discovery.async_load_platform('sensor', DOMAIN, {'sn': device_sn, 'type': ENTITY_TYPE_BATTERY, 'config_entry_id':entry.unique_id}, entry)
            )
        if(EufyApi.devices[device_sn].isMotionSensor):
            hass.async_create_task(
                hass.helpers.discovery.async_load_platform('binary_sensor', DOMAIN, {'sn': device_sn, 'type': ENTITY_TYPE_MOTION_SENSOR, 'config_entry_id':entry.unique_id}, entry)
            )
            
        pass
    return True