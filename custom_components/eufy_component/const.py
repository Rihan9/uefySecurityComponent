from eufySecurityApi.const import PARAM_TYPE, DEVICE_STATE

DOMAIN = "eufy_component"
DUMMY_DEVICE_ID = 'DUMMY_123'

TFA = 'Tfa'
EMAIL = 'Email'
PASSWORD = 'Password'
VERIFICATION_CODE = 'VC'

TFA_NONE = 'None'
TFA_EMAIL = 'Email'
TFA_SMS = 'Sms'
TFA_NOTIFICATION = 'Notification'

EUFY_TOKEN = 'Token'
EUFY_TOKEN_EXPIRE_AT = 'Token_expire_at'
EUFY_DOMAIN = 'Domain'

ENTITY_TYPE_BATTERY = 'Battery'
ENTITY_TYPE_MOTION_SENSOR = 'Motion_Sensor'

HASS_EUFY_API = 'Api'

SUBSCRIBE_PROPERTY = [
    PARAM_TYPE.BATTERY_LEVEL,
    PARAM_TYPE.PROP_STATUS,
    PARAM_TYPE.PROP_EVENT_NUM
]

USED_ENTITIES_DOMAIN = ['sensor', 'binary_sensor']