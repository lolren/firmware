# LongFast JSON Bridge

This repository is a LoRa JSON bridge project with two parts:

1. Firmware changes for a Heltec V3 node that add JSON chat + node-config endpoints.
2. A PC-hosted webserver/UI that proxies browser requests to the node.

The repository contains a full firmware tree because the firmware build system depends on it, but the custom bridge logic is isolated and documented below.

## Start Here

- Main guide: `LONGFAST_JSON_BRIDGE.md`
- Organized project entry: `longfast_json_bridge/README.md`
- Custom code map: `longfast_json_bridge/WHAT_IS_CUSTOM.md`

## Quick Run (PC Web UI)

```bash
./longfast_json_bridge/pc_webserver/run.sh 192.168.1.169
```

Open `http://127.0.0.1:8765`.

## Quick Flash (Heltec V3)

```bash
.venv/bin/pio run -e heltec-v3 -t upload --upload-port /dev/ttyUSB0
```

If Wi-Fi is not set yet, use USB CLI first (details in `longfast_json_bridge/firmware/README.md`).

## What Is Custom In This Repo

- Firmware endpoint registration and handlers:
  - `src/mesh/http/ContentHandler.cpp`
  - `src/mesh/http/ContentHandler.h`
- PC bridge server and browser UI:
  - `longfast_json_bridge/pc_webserver/longfast_json_bridge_web.py`
  - `longfast_json_bridge/pc_webserver/index.html`
  - `longfast_json_bridge/pc_webserver/run.sh`
- Bridge docs and setup:
  - `docs/longfast-json-bridge.md`
  - `docs/longfast-json-bridge-ui.md`
  - `docs/longfast-json-chat-api.md`
  - `docs/node-config-json-api.md`

## Endpoints Added By This Project

- `POST /json/chat/send`
- `GET /json/chat/messages`
- `GET /json/config/node`
- `POST /json/config/node`

## Notes

- This project is firmware-fork based.
- Security is LAN-trust oriented by default; do not expose these endpoints directly to the public internet.
