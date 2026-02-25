#!/usr/bin/env python3
"""
Local dev server — mirrors the Vercel Edge Middleware logic exactly.

Auth is accepted via either:
  1. HTTP Basic Auth header  →  used by the Screenly player
  2. screenly_demo_auth=1 cookie  →  set by the browser login form

Usage:
    python3 server.py
    open http://localhost:8080
"""

import base64
from http.server import HTTPServer, SimpleHTTPRequestHandler

USERNAME = "screenly"
PASSWORD = "admin"
COOKIE_NAME = "screenly_demo_auth"

VALID_TOKEN = "Basic " + base64.b64encode(
    f"{USERNAME}:{PASSWORD}".encode()
).decode()


class BasicAuthHandler(SimpleHTTPRequestHandler):

    def do_HEAD(self):
        if self._is_authorized():
            super().do_HEAD()
        else:
            self._send_401()

    def do_GET(self):
        if self._is_authorized():
            super().do_GET()
        else:
            self._send_401()

    def _is_authorized(self):
        # 1. Real HTTP Basic Auth (Screenly player)
        if self.headers.get("Authorization", "") == VALID_TOKEN:
            return True
        # 2. Session cookie (browser login form)
        cookies = self.headers.get("Cookie", "")
        if f"{COOKIE_NAME}=1" in cookies:
            return True
        return False

    def _send_401(self):
        body = b"401 Unauthorized - use the browser form or HTTP Basic Auth"
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Screenly Demo"')
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        auth = self.headers.get("Authorization", "—")
        cookies = self.headers.get("Cookie", "—")
        ok = self._is_authorized()
        print(f"[{'OK' if ok else 'DENIED'}] {self.command} {self.path}")


if __name__ == "__main__":
    port = 8080
    server = HTTPServer(("", port), BasicAuthHandler)
    print(f"Server: http://localhost:{port}")
    print(f"Credentials: {USERNAME} / {PASSWORD}")
    print(f"Expected header: {VALID_TOKEN}\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
