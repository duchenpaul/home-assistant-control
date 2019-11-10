# Home Assistant Control
Control Home Assistant devices in homekit, via homebridge-Http plugin.

## How it works
homebridge-Http requests url like `http://localhost:5001/midware/switch.phicomm_dc1_switch0?action=on`, this midware convert it into home assistant api request.

## Usage
run `gunicorn -D -w 1 -b 0.0.0.0:5010 homebridge_midware_app:app`

currently accept below 3 methods, "on/off/status":
```json
{
  "on_url": "http://<IP>/midware/switch.phicomm_dc1_switch0/on",
  "off_url": "http://<IP>/midware/switch.phicomm_dc1_switch0/off",
  "status_url": "http://<IP>/midware/switch.phicomm_dc1_switch0/status"
}
```

config demo:

```json
{
  "accessory": "Http",
  "name": "phicomm_dc1_switch0",
  "switchHandling": "no",
  "http_method": "GET",
  "on_url": "http://<IP>/midware/switch.phicomm_dc1_switch0/on",
  "off_url": "http://<IP>/midware/switch.phicomm_dc1_switch0/off",
  "status_url": "http://<IP>/midware/switch.phicomm_dc1_switch0/status",
  "status_on": "1",
  "status_off": "0",
  "service": "Switch",
  "sendimmediately": ""
}
```