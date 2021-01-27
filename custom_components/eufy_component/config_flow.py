from homeassistant import config_entries
from .const import DOMAIN, PASSWORD, EMAIL, TFA, TFA_NONE, TFA_EMAIL, TFA_SMS, TFA_NOTIFICATION, DUMMY_DEVICE_ID
from .const import VERIFICATION_CODE, EUFY_TOKEN, EUFY_TOKEN_EXPIRE_AT, EUFY_DOMAIN

from eufySecurityApi.api import Api, LoginException

import voluptuous as vol
import logging

_LOGGER = logging.getLogger(__name__)

class LoginFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    def init_step(self):
        _LOGGER.info('init_step')
        self.eufyApi = None

    async def async_step_user(self, info):
        _LOGGER.debug('step_user: start')
        if(info is not None):
            _LOGGER.debug('step_user: info')
            self.eufyApi = Api(
                username=info.get(EMAIL), 
                password=info.get(PASSWORD), 
                preferred2FAMethod=info.get(TFA)
            )
            try:
                response = await self.eufyApi.authenticate()
                _LOGGER.debug('step_user: response %s' % response)
                if(response == 'OK'):
                    _LOGGER.info('step_user: token %s, expire %s, domain %s ' % (self.eufyApi.token, self.eufyApi.token_expire_at, self.eufyApi.domain))
                    return self.async_create_entry(title="Eufy Security", data={
                        EUFY_TOKEN: self.eufyApi.token,
                        EUFY_TOKEN_EXPIRE_AT: self.eufyApi.token_expire_at,
                        EUFY_DOMAIN: self.eufyApi.domain
                    })
                else:
                    return self.async_abort(reason="login_error")
            # except LoginException as e:
            #     _LOGGER.exception(e)
            #     return self.async_abort(reason="login_error")
            except Exception as e:
                _LOGGER.exception(e)
                return self.async_abort(reason="login_error")
        else:
            _LOGGER.debug('step_user: show form')
            return self.async_show_form(
                step_id="user", data_schema=vol.Schema({
                    vol.Required(EMAIL): str, 
                    vol.Required(PASSWORD): str,
                    vol.Required(TFA): vol.In([TFA_NONE, TFA_EMAIL, TFA_SMS, TFA_NOTIFICATION])
                })
            )