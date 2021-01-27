from homeassistant import config_entries
from .const import DOMAIN, /
    PASSWORD, EMAIL, /
    TFA_NONE, TFA_EMAIL, TFA_SMS, TFA_NOTIFICATION

import voluptuous as vol
import logging

_LOGGER = logging.getLogger(__name__)
class LoginFlow(config_entries.ConfigFlow, domain=DOMAIN):
    
    async def async_step_user(self, info):
        if(info is not None):
            await self._config(info)
        else:
            return self.async_show_form(
                step_id="user", data_schema=vol.Schema({
                    vol.Required("Email"): str, 
                    vol.Required("password"): str,
                    vol.Required("two factor autentication"): vol.In([TFA_NONE, TFA_EMAIL, TFA_SMS, TFA_NOTIFICATION])
                })
            )
    
    async def _config(self, info):
        _LOGGER.warn(info)