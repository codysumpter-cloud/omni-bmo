#!/usr/bin/env python3
"""Local mock Reticulum bridge for Milestone K testing.

Run:
  python3 adapters/reticulum_bridge_mock.py --host 127.0.0.1 --port 8788

Then set in config.json:
  "reticulum_bridge_endpoint": "http://127.0.0.1:8788/bridge"
"""

from __future__ import annotations

import argparse
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: dict):
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        if self.path != "/bridge":
            self._send(404, {"error": "not_found"})
            return

        try:
            length = int(self.headers.get("content-length", "0"))
            body = self.rfile.read(length) if length > 0 else b"{}"
            req = json.loads(body.decode("utf-8", "ignore"))
        except Exception:
            self._send(400, {"error": "bad_json"})
            return

        mode = str(req.get("mode", ""))
        text = str(req.get("text", "")).strip()
        now = int(time.time())

        if mode != "reticulum_fallback":
            self._send(400, {"error": "bad_mode", "message": "expected reticulum_fallback"})
            return

        reply = {
            "text": f"[reticulum-mock:{now}] relay acknowledged: {text or 'empty message'}"
        }
        self._send(200, reply)

    def log_message(self, fmt, *args):
        # quiet default logs
        return


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8788)
    args = ap.parse_args()

    srv = HTTPServer((args.host, args.port), Handler)
    print(f"reticulum bridge mock listening on http://{args.host}:{args.port}/bridge")
    srv.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
