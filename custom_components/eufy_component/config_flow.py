from homeassistant import config_entries
from .const import DOMAIN
import voluptuous as vol


class LoginFlow(config_entries.ConfigFlow, domain=DOMAIN):
    
    async def async_step_user(self, info):
        if(info is not None):
            await self._config(info)
        else:
            return self.async_show_form(
                step_id="user", data_schema=vol.Schema({
                    vol.Required("Email"): str
                    vol.Required("password"): str
                    vol.Required("two factor autentication"): ['None', 'Email', 'Sms', 'Notification']
                })
            )