# What Is Custom

This file maps the bridge-specific code so you do not have to search the whole firmware tree.

## Architecture In One Line

Browser -> `localhost:8765` (PC proxy) -> node `/json/*` endpoints -> LoRa mesh packet flow.

## Firmware Custom Code

Primary file:

- `src/mesh/http/ContentHandler.cpp`

What is custom there:

- Registers custom routes in `registerHandlers(...)`:
  - `/json/config/node`
  - `/json/chat/send`
  - `/json/chat/messages`
- Implements endpoint handlers:
  - `handleJsonChatSend(...)`: validates JSON input and sends text packets over the mesh service.
  - `handleJsonNodeConfig(...)`: reads/updates owner name and Wi-Fi settings, persists to disk, optionally schedules reboot.
  - `handleJsonChatMessages(...)`: reads from `MessageStore`, filters by query params, returns JSON message list.
- Adds helper parsing/validation utilities for node IDs, booleans, content length bounds, and CORS headers.

Declarations:

- `src/mesh/http/ContentHandler.h`

Firmware defaults touched:

- `userPrefs.jsonc` (Wi-Fi defaults are intentionally not hardcoded with real credentials).

## PC Webserver Custom Code

Main files:

- `longfast_json_bridge/pc_webserver/longfast_json_bridge_web.py`
- `longfast_json_bridge/pc_webserver/index.html`
- `longfast_json_bridge/pc_webserver/run.sh`

What they do:

- Runs a local HTTP server on your PC (default `127.0.0.1:8765`).
- Proxies browser calls under `/api/*` to node `/json/*`.
- Accepts node address as full URL or bare IP/host (for example `192.168.1.169`).
- Hosts a UI for chat + node config.

Compatibility shim (legacy path):

- `tools/longfast_json_bridge/longfast_json_bridge_web.py`

## Core API Docs

- `docs/longfast-json-chat-api.md`
- `docs/node-config-json-api.md`
- `docs/longfast-json-bridge-ui.md`
- `docs/longfast-json-bridge.md`

## Why The Repo Still Looks Large

The firmware build requires the full upstream codebase.  
Bridge behavior is concentrated in the files listed above.
