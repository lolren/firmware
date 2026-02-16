# Firmware Side (LongFast JSON Bridge)

This branch adds JSON endpoints to the firmware core for chat + node config over Wi-Fi.

## Added Endpoints

- `POST /json/chat/send`
- `GET /json/chat/messages`
- `GET /json/config/node`
- `POST /json/config/node`

Implementation lives in:

- `src/mesh/http/ContentHandler.cpp`
- `src/mesh/http/ContentHandler.h`
- `longfast_json_bridge/WHAT_IS_CUSTOM.md` (file-level map)

## Build + Flash (Heltec V3)

```bash
cd <repo-root>
.venv/bin/pio run -e heltec-v3 -t upload --upload-port /dev/ttyUSB0
```

## Wi-Fi Bootstrap (USB CLI)

If web is not reachable yet, set Wi-Fi over USB first:

```bash
cd <repo-root>
.venv/bin/meshtastic --port /dev/ttyUSB0 \
  --set network.wifi_enabled true \
  --set network.wifi_ssid "YOUR_SSID" \
  --set network.wifi_psk "YOUR_PASSWORD" \
  --reboot
```

Get IP from serial logs:

```bash
stty -F /dev/ttyUSB0 115200 raw -echo -echoe -echok -echoctl -echoke
timeout 25s cat /dev/ttyUSB0 | strings | rg "Obtained IP address"
```

## Verify API

```bash
curl -sS http://<node-ip>/json/report
curl -sS http://<node-ip>/json/config/node
curl -sS "http://<node-ip>/json/chat/messages?limit=5"
```

## Notes

- Web server requires Wi-Fi or Ethernet enabled on the node.
- Use trusted local networks only; no built-in auth on these custom JSON endpoints.
