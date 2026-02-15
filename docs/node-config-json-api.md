# Node Config JSON API

Custom firmware endpoint for basic node configuration over Wi-Fi.

## Endpoint

- `GET /json/config/node`
- `POST /json/config/node`

## GET example

```bash
curl -sS http://<node-ip>/json/config/node
```

Example response:

```json
{
  "status": "ok",
  "data": {
    "owner": {
      "id": "!b03d5ec8",
      "long_name": "Meshtastic 5ec8",
      "short_name": "5ec8",
      "node_num": 2956811976
    },
    "wifi": {
      "enabled": true,
      "ssid": "YourWiFiSSID",
      "psk_set": true
    }
  }
}
```

## POST fields

All fields are optional, but at least one must be present.

- `longName` (string, max 39)
- `shortName` (string, max 4)
- `wifiEnabled` (bool)
- `wifiSsid` (string, max 32)
- `wifiPsk` (string, max 64)
- `reboot` (bool)
  - Default: `true` if Wi-Fi fields changed, otherwise `false`

## POST examples

Set name only, no reboot:

```bash
curl -sS -X POST http://<node-ip>/json/config/node \
  -H "Content-Type: application/json" \
  -d '{"longName":"My Heltec","shortName":"H3V3","reboot":false}'
```

Set Wi-Fi and reboot (recommended):

```bash
curl -sS -X POST http://<node-ip>/json/config/node \
  -H "Content-Type: application/json" \
  -d '{"wifiEnabled":true,"wifiSsid":"YourWiFiSSID","wifiPsk":"YourWiFiPassword","reboot":true}'
```

## Success response

```json
{
  "status": "ok",
  "data": {
    "owner_changed": true,
    "wifi_changed": true,
    "reboot_scheduled": true
  }
}
```
