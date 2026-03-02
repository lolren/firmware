# LongFast JSON Bridge Chat API (Heltec V3 Custom Firmware)

This firmware adds two JSON endpoints over Wi-Fi for text messaging:

- `POST /json/chat/send`
- `GET /json/chat/messages`

These endpoints let you build your own UI for channel (LongFast) and private chat without using the stock web app.

## Base URL

Use your node IP from serial logs (or `/json/report`):

- `http://<node-ip>/json/chat/send`
- `http://<node-ip>/json/chat/messages`

## 1) Send Message

`POST /json/chat/send`

### JSON body

- `text` (string, required): message text
- `channel` (number, optional): channel index, defaults to `0` (primary channel)
- `to` (number or string, optional): destination node
  - Omit for broadcast/channel message
  - Accepts decimal (`12345678`) or node id string (`"!0abc1234"`)
- `wantAck` (bool or string, optional): request ACK (`true`/`false`)
- `hopLimit` (number, optional): custom hop limit `0..255`

### Broadcast example (channel)

```bash
curl -sS -X POST "http://<node-ip>/json/chat/send" \
  -H "Content-Type: application/json" \
  -d '{"text":"hello LongFast","channel":0}'
```

### Private message example

```bash
curl -sS -X POST "http://<node-ip>/json/chat/send" \
  -H "Content-Type: application/json" \
  -d '{"text":"private ping","to":"!1234abcd","wantAck":true}'
```

### Success response

```json
{
  "status":"ok",
  "data":{
    "packet_id":123456789,
    "to":4294967295,
    "channel":0,
    "want_ack":false
  }
}
```

## 2) Read Messages

`GET /json/chat/messages`

Returns recent text messages stored by the device (incoming and outgoing).

### Query params

- `limit` (optional): number of messages, default `30`, max `100`
- `since` (optional): return only messages with `timestamp > since`
- `channel` (optional): filter by channel index
- `peer` (optional): filter private thread by peer node (`!hex` or decimal)
- `includeBroadcast` (optional): `true`/`false`
- `includeDm` (optional): `true`/`false`

### Poll latest messages

```bash
curl -sS "http://<node-ip>/json/chat/messages?limit=30"
```

### Poll only one private thread

```bash
curl -sS "http://<node-ip>/json/chat/messages?peer=!1234abcd&includeBroadcast=false"
```

### Response shape

```json
{
  "status":"ok",
  "data":{
    "count":2,
    "messages":[
      {
        "timestamp":1739610000,
        "is_boot_relative":false,
        "channel":0,
        "scope":"channel",
        "direction":"in",
        "sender_num":123,
        "sender_id":"!0000007b",
        "to_num":4294967295,
        "to_id":"!ffffffff",
        "peer_num":4294967295,
        "peer_id":"!ffffffff",
        "text":"hello"
      }
    ]
  }
}
```

## Frontend integration pattern

1. Keep `lastTimestamp` in your app.
2. Poll `GET /json/chat/messages?since=<lastTimestamp>&limit=100` every 1-3 seconds.
3. Render each message by `scope`:
   - `channel`: shared chat
   - `private`: DM thread (`peer_id`)
4. Send with `POST /json/chat/send`.

## Notes

- Channel index `0` is normally the primary channel (LongFast in default Meshtastic setups).
- Node IDs are hex with `!` prefix (for example `!1234abcd`).
- This API is plain HTTP inside your local network; add your own gateway/auth layer if exposed beyond LAN.
