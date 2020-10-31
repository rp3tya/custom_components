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
    vol.Optional(CONF_HOST, default='192.168.1.4'): cv.string,
    vol.Optional(CONF_PORT, default=3000): cv.port,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    from iMatic import devices
    # Assign configuration variables.
    # The configuration check takes care they are present.
    name = config[CONF_NAME]
    host = config[CONF_HOST]
    port = config[CONF_PORT]
    
    board = devices.EthernetRelay(host, port)

    # Add devices
    for rid in range(16):
        add_entities([SwitchIMatic(board, rid, 'Relay{0}'.format(rid))])
    
    # Setup services
    def all_on():
        board.all_on()
        for rid in range(16):
            hass.services.call('homeassistant', 'update_entity', {"entity_id":'switch.relay{0}'.format(rid)})
    def all_off():
        board.all_off()
        for rid in range(16):
            hass.services.call('homeassistant', 'update_entity', {"entity_id":'switch.relay{0}'.format(rid)})
    #
    hass.services.register('imatic', 'all_on', lambda call: all_on())
    hass.services.register('imatic', 'all_off', lambda call: all_off())


class SwitchIMatic(SwitchDevice):
    def __init__(self, relay, rid, name):
        """Initialize"""
        self._relay = relay
        self._rid = rid
        self._name = name
        self._state = None

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
        """Instruct the light to turn on."""
        self._relay.turn_on(self._rid)

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._relay.turn_off(self._rid)

    def update(self):
        """This is the only method that should fetch new data for Home Assistant."""
        self._state = self._relay.state()[self._rid]
        
