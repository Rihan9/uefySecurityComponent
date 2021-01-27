from homeassistant import config_entries
from .const import DOMAIN, PASSWORD, EMAIL, TFA, TFA_NONE, TFA_EMAIL, TFA_SMS, TFA_NOTIFICATION

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
                    vol.Required(EMAIL): str, 
                    vol.Required(PASSWORD): str,
                    vol.Required(TFA): vol.In([TFA_NONE, TFA_EMAIL, TFA_SMS, TFA_NOTIFICATION])
                })
            )
    
    async def _config(self, info):
        _LOGGER.warn(info)