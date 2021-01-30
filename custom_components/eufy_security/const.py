from eufySecurityApi.const import PARAM_TYPE, DEVICE_STATE, GUARD_MODE
from enum import Enum

DOMAIN = "eufy_security"

TFA = 'Tfa'
EMAIL = 'Email'
PASSWORD = 'Password'
VERIFICATION_CODE = 'VC'
CURRENT_FLOW = 'CF'
CURRENT_FLOW_USER = 'USER'
CURRENT_FLOW_REAUTH = 'REAUTH'

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
    PARAM_TYPE.PROP_EVENT_NUM,
    PARAM_TYPE.GUARD_MODE,
    PARAM_TYPE.SCHEDULE_MODE,
    PARAM_TYPE.DEVICE_RSSI,
    PARAM_TYPE.CAMERA_WIFI_RSSI
]

USED_ENTITIES_DOMAIN = ['sensor', 'binary_sensor']


PARAM_TYPE_TO_ENTITIES = {
    PARAM_TYPE.GUARD_MODE: ('sensor', 'impostazione allarme', 'mdi:shield'),
    PARAM_TYPE.DEVICE_RSSI: ('sensor', 'rssi connessione', 'mdi:wifi'),
    PARAM_TYPE.CAMERA_WIFI_RSSI: ('sensor', 'rssi connessione', 'mdi:wifi'),
    PARAM_TYPE.MOTION_SENSOR_PIR_SENSITIVITY: ('sensor', 'sensibilità al movimento', 'mdi:motion-sensor')
}