# LongFast JSON Bridge Endpoint Reference

This document covers both layers:

- Device firmware JSON endpoints on the node (`/json/*`)
- Local PC proxy/UI endpoints (`/api/*`) on `localhost:8765`

## 1) Firmware Endpoints (`http://<node-ip>/json/*`)

### `GET /json/report`

Returns device summary (owner, radio, build/version, etc).

Example:

```bash
curl -sS http://<node-ip>/json/report
```

### `GET /json/nodes`

Returns node/user list from firmware.

Typical query:

- `content=json`

Example:

```bash
curl -sS "http://<node-ip>/json/nodes?content=json"
```

### `GET /json/chat/messages`

Returns message history.

Supported query params:

- `limit` (default `30`, max `100`)
- `since` (unix timestamp)
- `channel`
- `peer`
- `includeBroadcast` (`true|false`)
- `includeDm` (`true|false`)

Example:

```bash
curl -sS "http://<node-ip>/json/chat/messages?limit=50&includeBroadcast=true&includeDm=true"
```

### `POST /json/chat/send`

Send channel or private text.

Request JSON:

- `text` (string, required)
- `channel` (number, optional, default `0`)
- `to` (number/string, optional; when set, send private)
- `wantAck` (bool/string, optional)
- `hopLimit` (number `0..255`, optional)

Examples:

```bash
# Channel message
curl -sS -X POST "http://<node-ip>/json/chat/send" \
  -H "Content-Type: application/json" \
  -d '{"text":"hello LongFast","channel":0}'

# Private message
curl -sS -X POST "http://<node-ip>/json/chat/send" \
  -H "Content-Type: application/json" \
  -d '{"text":"private ping","to":"!1234abcd","wantAck":true}'
```

### `GET /json/config/node`

Read owner + Wi-Fi config.

Example:

```bash
curl -sS http://<node-ip>/json/config/node
```

### `POST /json/config/node`

Update owner and/or Wi-Fi config.

Request JSON fields:

- `longName` (string, max 39)
- `shortName` (string, max 4)
- `wifiEnabled` (bool)
- `wifiSsid` (string, max 32)
- `wifiPsk` (string, max 64)
- `reboot` (bool)

Example:

```bash
curl -sS -X POST http://<node-ip>/json/config/node \
  -H "Content-Type: application/json" \
  -d '{"wifiEnabled":true,"wifiSsid":"YOUR_SSID","wifiPsk":"YOUR_PASSWORD","reboot":true}'
```

## 2) Local PC Proxy Endpoints (`http://127.0.0.1:8765/api/*`)

### `GET /api/config`

Returns current node base URL used by proxy.

Response:

```json
{"status":"ok","esp_base_url":"http://192.168.1.169"}
```

### `POST /api/config`

Update proxy target node URL.

Request JSON:

- `esp_base_url` (required): host/IP or full URL

Accepted examples:

- `192.168.1.169`
- `http://192.168.1.169`
- `meshtastic.local`

### `GET /api/report`

Proxy to firmware `GET /json/report`.

### `GET /api/nodes`

Proxy to firmware `GET /json/nodes`.

If no query is provided, proxy injects `content=json`.

### `GET /api/messages`

Proxy to firmware `GET /json/chat/messages` with query passthrough.

### `POST /api/send`

Proxy to firmware `POST /json/chat/send`.

### `GET /api/node-config`

Proxy to firmware `GET /json/config/node`.

### `POST /api/node-config`

Proxy to firmware `POST /json/config/node`.

### `OPTIONS /api/*`

CORS preflight handler.

## 3) Common Error Shapes

Firmware or proxy errors are returned as JSON:

```json
{"status":"error","error":"<code>","detail":"optional"}
```

Proxy-specific unreachable error:

```json
{
  "status":"error",
  "error":"esp_unreachable",
  "detail":"...",
  "esp_base_url":"http://192.168.1.169"
}
```

## 4) Related Detailed Docs

- `docs/longfast-json-chat-api.md`
- `docs/node-config-json-api.md`
- `docs/longfast-json-bridge-ui.md`
