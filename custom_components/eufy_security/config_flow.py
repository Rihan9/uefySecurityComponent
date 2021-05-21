from homeassistant import config_entries
from .const import (DOMAIN, PASSWORD, EMAIL, TFA, TFA_NONE, TFA_EMAIL, TFA_SMS, TFA_NOTIFICATION,
    VERIFICATION_CODE, EUFY_TOKEN, EUFY_TOKEN_EXPIRE_AT, EUFY_DOMAIN, CURRENT_FLOW, CURRENT_FLOW_REAUTH, CURRENT_FLOW_USER,
    TWO_FACTOR_AUTH_METHODS
)

from eufySecurityApi.api import Api, LoginException

import voluptuous as vol
import logging

from homeassistant.const import (
    CONF_EMAIL,
    CONF_PASSWORD,
)

_LOGGER = logging.getLogger(__name__)

class LoginFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    def init_step(self):
        _LOGGER.info('init_step')
        self.eufyApi = None
        self._firstReauthTry = False
    
    async def async_step_reauth(self, info):
        # info.set(CURRENT_FLOW, CURRENT_FLOW_REAUTH)
        info = dict(info)
        info[CURRENT_FLOW] = CURRENT_FLOW_REAUTH
        if(CONF_EMAIL in info):
            auth_state = await self._login(info.get(CONF_PASSWORD), info.get(CONF_EMAIL), TWO_FACTOR_AUTH_METHODS[info.get(TFA)])
            if(auth_state == 'OK'):
                existing_entry = await self.async_set_unique_id(self.eufyApi.userId)
                self.hass.config_entries.async_update_entry(
                    existing_entry, data={
                        EUFY_TOKEN: self.eufyApi.token,
                        EUFY_TOKEN_EXPIRE_AT: self.eufyApi.token_expire_at,
                        EUFY_DOMAIN: self.eufyApi.domain,
                        'unique_id': self.eufyApi.userId
                    }
                )
                return self.async_abort(reason="reauth_successful")
            elif(auth_state == 'send_verify_code'):
                return await self.async_step_twofactor(info)
            
            return self._login_form(email=info.get(CONF_EMAIL), password=info.get(CONF_PASSWORD), tfa=info.get(TFA), step_id='reauth', errors={"base": "login_error"})
        
        else:
            return self._login_form(step_id='reauth')
            

    async def async_step_user(self, info):
        if(info is not None):
            info = dict(info)
            info[CURRENT_FLOW] = CURRENT_FLOW_USER
        if(info is not None and not info.get('LOGIN_ERROR')):
            auth_state = await self._login(info.get(CONF_EMAIL), info.get(CONF_PASSWORD), TWO_FACTOR_AUTH_METHODS[info.get(TFA)])
            _LOGGER.info('auth_state: %s' % auth_state)
            if(auth_state == 'OK'):
                await self.async_set_unique_id(self.eufyApi.userId)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title='Eufy Security', data={
                        EUFY_TOKEN: self.eufyApi.token,
                        EUFY_TOKEN_EXPIRE_AT: self.eufyApi.token_expire_at,
                        EUFY_DOMAIN: self.eufyApi.domain,
                        'unique_id': self.eufyApi.userId
                    }
                )
            elif(auth_state == 'send_verify_code'):
                return await self.async_step_twofactor(info)
            # auth_state incorrect
            # return self._login_form(email=info.get(EMAIL), password=info.get(PASSWORD), tfa=info.get(TFA), step_id='reauth')
            info['LOGIN_ERROR'] = True
            
            return self._login_form(step_id='user', errors={"base": "login_error"})
        else:
            return self._login_form(step_id='user')
        
    async def async_step_twofactor(self, info):
        if(VERIFICATION_CODE not in info):
            return self.async_show_form(step_id='twofactor', data_schema=vol.Schema({
                    vol.Required(VERIFICATION_CODE): str
                }))
        response = await self.eufyApi.sendVerifyCode(info.get(VERIFICATION_CODE))
        if(response == 'OK'):
            if(info.get(CURRENT_FLOW) == CURRENT_FLOW_REAUTH):
                existing_entry = await self.async_set_unique_id(self.eufyApi.userId)
                self.hass.config_entries.async_update_entry(
                    existing_entry, data={
                        EUFY_TOKEN: self.eufyApi.token,
                        EUFY_TOKEN_EXPIRE_AT: self.eufyApi.token_expire_at,
                        EUFY_DOMAIN: self.eufyApi.domain,
                        'unique_id': self.eufyApi.userId
                    }
                )
                return self.async_abort(reason="reauth_successful")
            else:
                return self.async_create_entry(
                    title='Eufy Security', data={
                        EUFY_TOKEN: self.eufyApi.token,
                        EUFY_TOKEN_EXPIRE_AT: self.eufyApi.token_expire_at,
                        EUFY_DOMAIN: self.eufyApi.domain,
                        'unique_id': self.eufyApi.userId
                    }
                )
            pass
        else:
            return self.async_show_form(step_id='twofactor', data_schema=vol.Schema({
                vol.Required(VERIFICATION_CODE): str
            }), errors={"base": "verification_code_error"})



    
    async def _auth_flow(self, info, abortIfConfigurated=True):
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
                    
                    await self.async_set_unique_id(self.eufyApi.userId)
                    if(abortIfConfigurated):
                        self._abort_if_unique_id_configured()

                    _LOGGER.info('step_user: token %s, expire %s, domain %s ' % (self.eufyApi.token, self.eufyApi.token_expire_at, self.eufyApi.domain))
                    return self.async_create_entry(title="Eufy Security", data={
                        EUFY_TOKEN: self.eufyApi.token,
                        EUFY_TOKEN_EXPIRE_AT: self.eufyApi.token_expire_at,
                        EUFY_DOMAIN: self.eufyApi.domain,
                        EMAIL: info.get(EMAIL),
                        PASSWORD: info.get(PASSWORD),
                        TFA: info.get(TFA),
                        'unique_id': self.eufyApi.userId
                    })
                else:
                    return self.async_abort(reason="login_error")
            # except LoginException as e:
            #     _LOGGER.exception(e)
            #     return self.async_abort(reason="login_error")
            except Exception as e:
                _LOGGER.ERROR('auth failed %s' % e)
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

    async def _login(self, email, password, tfa):
        self.eufyApi = Api(
            username=email, 
            password=password, 
            preferred2FAMethod=tfa
        )
        try:
            response = await self.eufyApi.authenticate()
            return response
        except Exception as e:
            _LOGGER.exception(e)
            return 'KO'


    def _login_form(self, email=None, password=None, tfa=None, step_id="user", **kwargs):
        if kwargs is None:
            kwargs = {}
        kwargs['step_id'] = step_id
        kwargs['data_schema'] = vol.Schema({
                vol.Required(CONF_EMAIL, default=email): str, 
                vol.Required(CONF_PASSWORD, default=password): str,
                vol.Required(TFA, default=tfa): vol.In([TFA_NONE, TFA_EMAIL, TFA_SMS, TFA_NOTIFICATION])
            })
        
        return self.async_show_form(**kwargs)
