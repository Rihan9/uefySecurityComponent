from .const import PARAM_TYPE, GUARD_MODE, POWER_MODE

def wrap(device, attribute):

    switch = {
        PARAM_TYPE.GUARD_MODE:
            lambda : GUARD_MODE(device.attribute[attribute]).name.lower().replace('_', ' ') 
                if device.attribute[attribute] != GUARD_MODE.SCHEDULED.value 
                else 'scheduled mode: ' + GUARD_MODE(device.attribute[PARAM_TYPE.SCHEDULE_MODE]).name.lower().replace('_', ' ') 
        , PARAM_TYPE.POWER_MODE:
            lambda: POWER_MODE(device.attribute[attribute]).name.lower().replace('_', ' ') 
    }
    if(attribute in switch):
        return switch[attribute]()
    else:
        return device.attribute[attribute]

    pass