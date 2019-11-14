import voluptuous as vol

import homeassistant.helpers.config_validation as cv

DOMAIN = 'chatin'

CONF_JID = 'jid'
CONF_PWD = 'password'
CONF_TLS = 'tls'
CONF_EID = 'entity'

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_JID): cv.string,
                vol.Required(CONF_PWD): cv.string,
                vol.Required(CONF_TLS): cv.boolean,
                vol.Required(CONF_EID): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

def setup(hass, config):
    from sleekxmpp import ClientXMPP
    from sleekxmpp.exceptions import IqError, IqTimeout

    class EchoBot(ClientXMPP):
        def __init__(self, jid, password, ha, eid):
            ClientXMPP.__init__(self, jid, password)
            self.add_event_handler("session_start", self.session_start)
            self.add_event_handler("message", self.message)
            self.ha = ha
            self.eid = eid
        def session_start(self, event):
            self.send_presence()
            self.get_roster()
        def message(self, msg):
            if msg['type'] in ('chat', 'normal'):
                self.ha.states.set(self.eid, '')
                self.ha.states.set(self.eid, "{}".format("%(body)s" % msg))

    conf = config[DOMAIN]
    jid = conf.get(CONF_JID)
    pwd = conf.get(CONF_PWD)
    tls = conf.get(CONF_TLS)
    eid = conf.get(CONF_EID)

    xmpp = EchoBot(jid, pwd, hass, eid)
    xmpp.connect(use_tls=tls)
    xmpp.process(block=False, forever=True)

    return True
