"""Small dependency-free health endpoint used until service implementations land."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os

SERVICE_NAME = os.environ.get("SERVICE_NAME", "service")
PORT = int(os.environ.get("PORT", "8080"))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 - required by BaseHTTPRequestHandler
        if self.path not in ("/health", "/healthz"):
            self.send_error(404)
            return
        payload = json.dumps({"service": SERVICE_NAME, "status": "ok"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *_args):
        return

ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
