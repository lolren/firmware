# LongFast JSON Bridge

`LongFast JSON Bridge` is a Meshtastic firmware extension + local web interface for JSON-first chat and node control over Wi-Fi.

It is designed for users who want to build custom interfaces without depending on the stock web client.

## What It Adds

Firmware endpoints:

- `POST /json/chat/send`
- `GET /json/chat/messages`
- `GET /json/config/node`
- `POST /json/config/node`

Local UI bundle:

- `tools/longfast_json_bridge/longfast_json_bridge_web.py`
- `tools/longfast_json_bridge/index.html`

## Features

- Channel (LongFast) messaging via JSON
- Private messaging via JSON
- Message polling and filtering
- Node list with names and IDs
- Right-click quick actions for DM workflows
- Node name + Wi-Fi configuration from browser

## Security Notes

- This API is intended for trusted local networks.
- No auth layer is built into these custom endpoints.
- Do not expose these endpoints directly to the internet.

## Replication Guide

### 1) Clone and build

```bash
git clone https://github.com/meshtastic/firmware.git
cd firmware
pio run -e heltec-v3
```

### 2) Configure Wi-Fi (no hardcoded credentials in repo)

Option A: set compile-time defaults in `userPrefs.jsonc` before build:

- `USERPREFS_NETWORK_WIFI_ENABLED`
- `USERPREFS_NETWORK_WIFI_SSID`
- `USERPREFS_NETWORK_WIFI_PSK`

Option B: flash first, then configure over your existing management path (app/serial), then use `/json/config/node` after Wi-Fi is up.

### 3) Flash firmware

```bash
pio run -e heltec-v3 -t upload --upload-port /dev/ttyUSB0
```

### 4) Verify API

```bash
curl -sS http://<node-ip>/json/report
curl -sS http://<node-ip>/json/chat/messages?limit=5
```

### 5) Start the local bridge UI

```bash
python3 tools/longfast_json_bridge/longfast_json_bridge_web.py \
  --host 0.0.0.0 \
  --port 8765 \
  --esp-base-url http://<node-ip>
```

Open `http://127.0.0.1:8765`.

## Documentation Map

- Chat API: `docs/longfast-json-chat-api.md`
- Node Config API: `docs/node-config-json-api.md`
- Web UI usage: `docs/longfast-json-bridge-ui.md`
- Explainer video script + generator: `docs/longfast-json-bridge-video.md`

## Known Constraints

- Message history is backed by `MessageStore` in firmware; availability depends on build flags/platform behavior.
- Wi-Fi changes are safest with reboot enabled.
