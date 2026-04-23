#!/usr/bin/env python3
"""
Local HTTP service for Xiaohongshu clipping.

Starts a small server on 127.0.0.1:7895 by default. It accepts a Xiaohongshu
post URL and forwards it to clipper.py.
"""
from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(__file__.rsplit("/", 1)[0]))
from clipper import clip, log  # noqa: E402

HOST = os.getenv("XHS_HOST", "127.0.0.1")
PORT = int(os.getenv("XHS_PORT", "7895"))


class Handler(BaseHTTPRequestHandler):
    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, code: int, data: dict) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._json(200, {"ok": True, "service": "xhs-clipper", "port": PORT})
            return
        if parsed.path == "/clip":
            params = parse_qs(parsed.query)
            url = (params.get("url") or [""])[0]
            if not url:
                self._json(400, {"success": False, "error": "missing url"})
                return
            result = clip(url)
            self._json(200 if result.get("success") else 500, result)
            return
        self._json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path != "/clip":
            self._json(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        try:
            data = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            self._json(400, {"success": False, "error": "invalid json"})
            return
        url = data.get("url", "")
        if not url:
            self._json(400, {"success": False, "error": "missing url"})
            return
        result = clip(url)
        self._json(200 if result.get("success") else 500, result)

    def log_message(self, fmt: str, *args) -> None:
        log(f"{self.address_string()} {fmt % args}")


def main() -> None:
    server = HTTPServer((HOST, PORT), Handler)
    log(f"Service started: http://{HOST}:{PORT}")
    log(f"Health check: http://{HOST}:{PORT}/health")
    log("Clip API: POST /clip  body={\"url\":\"https://www.xiaohongshu.com/explore/...\"}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("Service stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
