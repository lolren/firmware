# LongFast JSON Bridge Setup

This folder organizes the custom project into two parts:

- `pc_webserver/`: local browser UI + Python proxy that talks to the node JSON API.
- `firmware/`: firmware-specific notes (what changed, build/flash, and Wi-Fi bootstrap).

Workspace separation:

- Meshtastic/LongFast custom repo: `/home/lolren/Desktop/Meshtastic-json/firmware`
- MeshCore custom repo: `/home/lolren/Desktop/MeshCore-sideby/meshcore`

If you want the exact file-level map of custom code, read:

- `longfast_json_bridge/WHAT_IS_CUSTOM.md`
- `longfast_json_bridge/API_ENDPOINTS.md` (full endpoint reference)

Why the repo still looks large:

- firmware build requires the full source tree.
- bridge-specific behavior is concentrated in the files listed in `WHAT_IS_CUSTOM.md`.

## Quick Start

1. Flash firmware (see `firmware/README.md`).
2. Make sure the node has Wi-Fi credentials and is reachable by IP.
3. Start the PC bridge:

```bash
./longfast_json_bridge/pc_webserver/run.sh http://<node-ip>
```

You can also pass a bare host/IP like `192.168.1.169`.

4. Open:

- `http://localhost:8765`

## Repo Paths (Current)

- PC webserver code: `longfast_json_bridge/pc_webserver/`
- Firmware implementation changes:
  - `src/mesh/http/ContentHandler.cpp`
  - `src/mesh/http/ContentHandler.h`
  - `userPrefs.jsonc`
- API and usage docs:
  - `longfast_json_bridge/API_ENDPOINTS.md`
  - `docs/longfast-json-bridge.md`
  - `docs/longfast-json-bridge-ui.md`
  - `docs/longfast-json-chat-api.md`
  - `docs/node-config-json-api.md`

## Backward Compatibility

Legacy launcher path still works:

- `tools/longfast_json_bridge/longfast_json_bridge_web.py`

It now forwards to the new location in `longfast_json_bridge/pc_webserver/`.
