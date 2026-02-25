#!/usr/bin/env python3
"""
Local dev server with HTTP Basic Auth for Screenly Basic Auth demo.

Usage:
    python3 server.py

Then open: http://localhost:8080
Credentials: screenly / admin

The Screenly player sends:
    Authorization: Basic c2NyZWVubHk6YWRtaW4=
    (base64 of "screenly:admin")
"""

import base64
from http.server import HTTPServer, SimpleHTTPRequestHandler

USERNAME = "screenly"
PASSWORD = "admin"

VALID_TOKEN = "Basic " + base64.b64encode(
    f"{USERNAME}:{PASSWORD}".encode()
).decode()

UNAUTHORIZED_HTML = b"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>401 Unauthorized</title>
  <style>
    body { font-family: system-ui, sans-serif; display: flex; align-items: center;
           justify-content: center; min-height: 100vh; margin: 0; background: #f8f9fb; }
    .box { text-align: center; padding: 48px; border: 1px solid #e5e7eb;
           border-radius: 12px; background: #fff; }
    h1   { font-size: 20px; margin-bottom: 8px; color: #1a1a1a; }
    p    { font-size: 14px; color: #6b7280; }
  </style>
</head>
<body>
  <div class="box">
    <h1>401 Unauthorized</h1>
    <p>Valid Basic Auth credentials are required.</p>
  </div>
</body>
</html>"""


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
        return self.headers.get("Authorization", "") == VALID_TOKEN

    def _send_401(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Screenly Demo"')
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(UNAUTHORIZED_HTML)))
        self.end_headers()
        self.wfile.write(UNAUTHORIZED_HTML)

    def log_message(self, fmt, *args):
        auth = self.headers.get("Authorization", "none")
        status = "OK" if self._is_authorized() else "DENIED"
        print(f"[{status}] {self.command} {self.path}  |  Auth: {auth[:30]}...")


if __name__ == "__main__":
    port = 8080
    server = HTTPServer(("", port), BasicAuthHandler)
    print(f"Screenly Basic Auth demo server running on http://localhost:{port}")
    print(f"Credentials: {USERNAME} / {PASSWORD}")
    print(f"Authorization header value: {VALID_TOKEN}")
    print("Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
