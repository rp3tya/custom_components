import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
# Import the device class from the component that you want to support
from homeassistant.components.switch import (PLATFORM_SCHEMA, SwitchDevice)
from homeassistant.const import CONF_NAME, CONF_HOST, CONF_PORT

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default=1): cv.port,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    # Assign configuration variables.
    # The configuration check takes care they are present.
    name = config[CONF_NAME]
    host = config[CONF_HOST]
    port = config[CONF_PORT]
    # Add devices
    add_entities([SwitchLazybone(name, host, port)])

    # Setup services
    def on_off():
        import time
        import bluetooth
        sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        sock.connect((host,port))
        sock.send("e")
        time.sleep(1)
        sock.send("o") 
        sock.close()
    #
    hass.services.register('lazybone', 'on_off', lambda call: on_off())

class SwitchLazybone(SwitchDevice):
    def __init__(self, name, host, port):
        """Initialize"""
        self._name = name
        self._host = host
        self._port  = port
        self._state = False

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def available(self):
        """Return true if light switch is on."""
        return self._state is not None

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs):
        import bluetooth
        """Instruct the light to turn on."""
        sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        sock.connect((self._host,self._port))
        sock.send("e") 
        sock.close()
        self._state = True

    def turn_off(self, **kwargs):
        import bluetooth
        """Instruct the light to turn off."""
        sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        sock.connect((self._host,self._port))
        sock.send("o") 
        sock.close()
        self._state = False

    def update(self):
        """This is the only method that should fetch new data for Home Assistant."""
        self._state = self._state


