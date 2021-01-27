from homeassistant import config_entries
from .const import DOMAIN, PASSWORD, EMAIL, TFA, TFA_NONE, TFA_EMAIL, TFA_SMS, TFA_NOTIFICATION, DUMMY_DEVICE_ID
from .const import VERIFICATION_CODE, TOKEN, TOKEN_EXPIRE_AT, DOMAIN

from eufySecurityApi.api import Api, LoginException

import voluptuous as vol
import logging

_LOGGER = logging.getLogger(__name__)
class LoginFlow(config_entries.ConfigFlow, domain=DOMAIN):
    def __init__(self):
        super.__init__()
        self.eufyApi = None
    async def async_step_user(self, info):
        if(info is not None):
            return await self.async_step_tfa(info)
        else:
            await self.async_set_unique_id(DUMMY_DEVICE_ID)
            self._abort_if_unique_id_configured()

            return self.async_show_form(
                step_id="user", data_schema=vol.Schema({
                    vol.Required(EMAIL): str, 
                    vol.Required(PASSWORD): str,
                    vol.Required(TFA): vol.In([TFA_NONE, TFA_EMAIL, TFA_SMS, TFA_NOTIFICATION])
                })
            )
    
    async def async_step_tfa(self, info):
        if(info.get(VERIFICATION_CODE)):
            return self.async_abort(reason="not_supported")
            # return True
        if(info.get(TFA) == TFA_NONE):
            info.set(TFA, TFA_EMAIL)
        self.eufyApi = Api(
            username=info.get(EMAIL), 
            password=info.get(PASSWORD), 
            preferred2FAMethod=info.get(TFA)
        )
        try:
            response = self.eufyApi.authenticate()
            if(response == 'OK'):
                return self.async_create_entry(title="Eufy Security", data={
                    TOKEN: self.eufyApi.token,
                    TOKEN_EXPIRE_AT: self.eufyApi.token_expire_at,
                    DOMAIN: self.eufyApi.domain
                })
            elif('send_verify_code'):
                return self.async_show_form(
                step_id="tfa", data_schema=vol.Schema({
                    vol.Required(VERIFICATION_CODE): str
                })
            )
        except LoginException as e:
            _LOGGER.exception(e)
            return self.async_abort(reason="login_error")