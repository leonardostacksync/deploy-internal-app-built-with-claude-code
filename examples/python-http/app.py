"""A minimal internal app that follows the platform rules.

- listens on 0.0.0.0 and on the PORT the platform provides
- has a health check
- reads configuration from environment variables, never from the source
"""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            body, kind = json.dumps({"status": "ok"}).encode(), "application/json"
        else:
            title = os.environ.get("APP_TITLE", "Internal app")
            body = f"<!doctype html><title>{title}</title><h1>{title}</h1><p>Deployed with the EOS CLI.</p>".encode()
            kind = "text/html; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # keep logs quiet
        pass


def make_server(port: int, host: str = "0.0.0.0") -> HTTPServer:
    return HTTPServer((host, port), Handler)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))  # the platform supplies PORT at run time
    print(f"listening on 0.0.0.0:{port}")
    make_server(port).serve_forever()
