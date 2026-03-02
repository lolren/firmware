# LongFast JSON Bridge UI

`LongFast JSON Bridge` is a local Python web app that provides:

- Channel chat (LongFast) send/receive
- Private message send/receive
- Right-click node actions (DM target/filter/send/copy)
- Basic node config (name + Wi-Fi) through JSON

It runs on your PC and proxies requests to the node JSON API over LAN.

## Files

- `longfast_json_bridge/pc_webserver/longfast_json_bridge_web.py`
- `longfast_json_bridge/pc_webserver/index.html`

## Start the UI server

```bash
cd <repo-root>
python3 longfast_json_bridge/pc_webserver/longfast_json_bridge_web.py \
  --host 0.0.0.0 \
  --port 8765 \
  --esp-base-url http://<node-ip>
```

Open in browser:

- `http://127.0.0.1:8765`
- `http://<this-pc-ip>:8765` (from another LAN device)

## Chat usage

### LongFast channel

- Set `Channel Index` (usually `0`)
- Write text
- Click `Send Channel`

### Private message

- Set `Private To` (example: `!1234abcd`)
- Keep `wantAck` checked
- Click `Send Private`

### Faster DM flow

- In `Known Nodes`, right-click target node
- Use actions:
  - `Set As Private Target`
  - `Set DM Target + Filter`
  - `Send Private Using Current Text`
  - `Open DM Thread View`
  - `Copy Node ID`

## Node configuration usage

In `Node Config (Name + WiFi)`:

- Click `Load Node Config`
- Edit fields:
  - `Long Name` (max 39)
  - `Short Name` (max 4)
  - `wifiEnabled`
  - `WiFi SSID`
  - `WiFi PSK` (only when `update wifiPsk` is checked)
- Keep `reboot after save` checked when changing Wi-Fi
- Click `Save Node Config`

## Backend proxy routes

The UI calls local routes on the Python server:

- `GET/POST /api/config`
- `GET /api/report`
- `GET /api/nodes`
- `GET/POST /api/node-config`
- `GET /api/messages`
- `POST /api/send`
