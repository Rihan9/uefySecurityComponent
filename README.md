# Eufy Security Integrations for Home Assistant

## Installation

### Install from HACS:

- Add this repository (https://github.com/Rihan9/uefySecurityComponent) on your hacs installation (Category: Integration) and search for "Eufy Security" integration.
- After restart of home assistant go in setup -> Integration -> Add -> "Eufy Security".
- You need to insert your credentials for Eufy Security and your prefered two factor authentication method. 

#### PLEASE NOTE: 
- the two factor authentication is required if you don't want to relogin every month
- the two factor authentication method selected need to be configurated on the official app. Please refer to Official eufy manual to do it.
- if you don't want to use 2FA, you can select "None", but make sure it's turned off in the app too. Otherwise the 2fa is mandatory and the standard email method will be used.


## TODO:
- [ ] add attribute to monitor charge state (disconnected, charged, charged complete maybe?) 
- [X] correct the names of the sensor entity derived from device attribute in order to add device name at the beginning 
