#!/usr/bin/env python3
"""LongFast JSON Bridge web proxy for Meshtastic JSON endpoints."""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib import error, parse, request

DEFAULT_TIMEOUT_SEC = 8.0
MAX_REQUEST_BODY = 4096
INDEX_HTML = Path(__file__).with_name("index.html")


@dataclass
class AppState:
    esp_base_url: str


def sanitize_base_url(raw: str) -> str:
    value = raw.strip().rstrip("/")
    if not value:
        raise ValueError("esp_base_url is required")

    # Allow entering just "192.168.1.100" or "meshtastic.local"
    if "://" not in value:
        value = f"http://{value}"

    parsed = parse.urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(
            "esp_base_url must be a host/IP or URL, for example 192.168.1.100 or http://192.168.1.100"
        )

    # Keep only scheme + host[:port] so accidental paths/queries don't break proxy routes.
    return f"{parsed.scheme}://{parsed.netloc}"


class JsonChatHandler(BaseHTTPRequestHandler):
    state = AppState("http://192.168.1.100")
    index_html = INDEX_HTML.read_bytes() if INDEX_HTML.exists() else b""

    def log_message(self, fmt: str, *args: Any) -> None:
        logging.info("%s - %s", self.address_string(), fmt % args)

    def do_OPTIONS(self) -> None:
        if self.path.startswith("/api/"):
            self.send_response(204)
            self._set_json_headers()
            self.end_headers()
            return
        self.send_error(404)

    def do_GET(self) -> None:
        parsed = parse.urlsplit(self.path)

        if parsed.path in {"/", "/index.html"}:
            if not self.index_html:
                self._send_json(500, {"status": "error", "error": "missing_index_html"})
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(self.index_html)))
            self.end_headers()
            self.wfile.write(self.index_html)
            return

        if parsed.path == "/api/config":
            self._send_json(200, {"status": "ok", "esp_base_url": self.state.esp_base_url})
            return

        if parsed.path == "/api/report":
            status, payload = self._proxy_json("GET", "/json/report")
            self._send_json(status, payload)
            return

        if parsed.path == "/api/node-config":
            status, payload = self._proxy_json("GET", "/json/config/node")
            self._send_json(status, payload)
            return

        if parsed.path == "/api/messages":
            status, payload = self._proxy_json("GET", "/json/chat/messages", query=parsed.query)
            self._send_json(status, payload)
            return

        if parsed.path == "/api/nodes":
            query = parsed.query if parsed.query else "content=json"
            status, payload = self._proxy_json("GET", "/json/nodes", query=query)
            self._send_json(status, payload)
            return

        self._send_json(404, {"status": "error", "error": "not_found"})

    def do_POST(self) -> None:
        parsed = parse.urlsplit(self.path)

        if parsed.path == "/api/config":
            body = self._read_json_body()
            if body is None:
                return

            raw_url = body.get("esp_base_url")
            if not isinstance(raw_url, str) or not raw_url.strip():
                self._send_json(400, {"status": "error", "error": "field_esp_base_url_required"})
                return
            try:
                self.state.esp_base_url = sanitize_base_url(raw_url)
            except ValueError as exc:
                self._send_json(400, {"status": "error", "error": "field_esp_base_url_invalid", "detail": str(exc)})
                return

            self._send_json(200, {"status": "ok", "esp_base_url": self.state.esp_base_url})
            return

        if parsed.path == "/api/send":
            body = self._read_json_body()
            if body is None:
                return
            status, payload = self._proxy_json("POST", "/json/chat/send", payload=body)
            self._send_json(status, payload)
            return

        if parsed.path == "/api/node-config":
            body = self._read_json_body()
            if body is None:
                return
            status, payload = self._proxy_json("POST", "/json/config/node", payload=body)
            self._send_json(status, payload)
            return

        self._send_json(404, {"status": "error", "error": "not_found"})

    def _set_json_headers(self) -> None:
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")

    def _send_json(self, status_code: int, payload: dict[str, Any]) -> None:
        raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        self.send_response(status_code)
        self._set_json_headers()
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        try:
            self.wfile.write(raw)
        except (BrokenPipeError, ConnectionResetError):
            logging.debug("Client disconnected while sending JSON response")

    def _read_json_body(self) -> dict[str, Any] | None:
        content_length = self.headers.get("Content-Length", "")
        try:
            body_size = int(content_length)
        except ValueError:
            self._send_json(400, {"status": "error", "error": "invalid_content_length"})
            return None

        if body_size <= 0:
            self._send_json(400, {"status": "error", "error": "missing_body"})
            return None
        if body_size > MAX_REQUEST_BODY:
            self._send_json(413, {"status": "error", "error": "body_too_large"})
            return None

        raw = self.rfile.read(body_size)
        try:
            parsed: Any = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(400, {"status": "error", "error": "invalid_json"})
            return None

        if not isinstance(parsed, dict):
            self._send_json(400, {"status": "error", "error": "json_object_required"})
            return None

        return parsed

    def _proxy_json(self, method: str, path: str, query: str = "", payload: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
        url = f"{self.state.esp_base_url}{path}"
        if query:
            url = f"{url}?{query}"

        data = None
        headers = {"Accept": "application/json"}
        if payload is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(payload, separators=(",", ":")).encode("utf-8")

        req = request.Request(url=url, data=data, headers=headers, method=method)
        try:
            with request.urlopen(req, timeout=DEFAULT_TIMEOUT_SEC) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                parsed = json.loads(raw) if raw else {}
                if isinstance(parsed, dict):
                    return int(resp.status), parsed
                return int(resp.status), {"status": "error", "error": "non_object_response", "raw": parsed}
        except error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                parsed = {"status": "error", "error": "esp_http_error", "detail": raw[:300]}
            if not isinstance(parsed, dict):
                parsed = {"status": "error", "error": "esp_http_error", "detail": str(parsed)}
            return int(exc.code), parsed
        except (TimeoutError, OSError, error.URLError) as exc:
            return 502, {
                "status": "error",
                "error": "esp_unreachable",
                "detail": str(exc),
                "esp_base_url": self.state.esp_base_url,
            }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve LongFast JSON Bridge web UI for Meshtastic JSON endpoints")
    parser.add_argument("--host", default="127.0.0.1", help="Host/IP to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8765, help="HTTP port (default: 8765)")
    parser.add_argument(
        "--esp-base-url",
        default="http://192.168.1.100",
        help="Target Meshtastic node base URL (default: http://192.168.1.100)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        JsonChatHandler.state = AppState(esp_base_url=sanitize_base_url(args.esp_base_url))
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if not INDEX_HTML.exists():
        raise SystemExit(f"Missing UI file: {INDEX_HTML}")

    JsonChatHandler.index_html = INDEX_HTML.read_bytes()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    with ThreadingHTTPServer((args.host, args.port), JsonChatHandler) as server:
        logging.info("Local UI running at http://%s:%d", args.host, args.port)
        logging.info("Forwarding to Meshtastic node at %s", JsonChatHandler.state.esp_base_url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            logging.info("Stopping server")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
