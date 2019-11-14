Connects to an XMPP server and feeds every incoming message into a HA entity.

Sample configuration entry:
```
chatin:
  jid: !secret xmpp_jid
  password: !secret xmpp_pass
  tls: no
  entity: input_text.xmpp_message
```

Automations can then be created to trigger actions when certain message is received:
```
- alias: "Incoming message"
  trigger:
    - platform: state
      entity_id: input_text.xmpp_message
  action:
  - service: notify.TV
    data_template:
      title: "Incoming message"
      message: "{{trigger.to_state.state}}"
```
