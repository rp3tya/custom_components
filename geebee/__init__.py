import voluptuous as vol

import homeassistant.helpers.config_validation as cv

DOMAIN = 'geebee'

CONF_EID = 'entity'

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_EID): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

def setup(hass, config):
    import threading
    
    class GeeBeeThread(threading.Thread):
        def __init__(self, ha, eid):
            super(GeeBeeThread, self).__init__()
            self._ha = ha
            self._eid = eid
        def run(self):
            import bluetooth
            sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
            sock.bind(("",1))
            sock.listen(1)
            while True:
                client_sock,address = sock.accept()
                data = client_sock.recv(128)
                client_sock.close()
                self._ha.states.set(self._eid, '')
                self._ha.states.set(self._eid, " ".join(data.decode().splitlines()))
    
    conf = config[DOMAIN]
    eid = conf.get(CONF_EID)

    gb = GeeBeeThread(hass, eid)
    gb.start()

    return True

