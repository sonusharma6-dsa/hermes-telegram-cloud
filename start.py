import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from hermes_cli.gateway import run_gateway

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Hermes Telegram Gateway is Live!")

    def log_message(self, format, *args):
        pass  # Silence HTTP access logs

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"Render Health Server listening on port {port}...")
    server.serve_forever()

if __name__ == "__main__":
    # Start health check server thread for Render Free Web Service
    threading.Thread(target=run_health_server, daemon=True).start()

    print("Starting Hermes Gateway on Render Cloud...")
    run_gateway(verbose=1, quiet=False, replace=True, force=True)
