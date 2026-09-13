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

def setup_kaggle():
    api_token = os.environ.get("KAGGLE_API_TOKEN")
    username = os.environ.get("KAGGLE_USERNAME")
    key = os.environ.get("KAGGLE_KEY")

    kaggle_dir = os.path.expanduser("~/.kaggle")
    os.makedirs(kaggle_dir, exist_ok=True)

    if api_token:
        token_path = os.path.join(kaggle_dir, "access_token")
        with open(token_path, "w") as f:
            f.write(api_token.strip())
        print("Configured Kaggle API access token.")

    if username and key:
        json_path = os.path.join(kaggle_dir, "kaggle.json")
        import json
        with open(json_path, "w") as f:
            json.dump({"username": username, "key": key}, f)
        print("Configured Kaggle legacy json credentials.")

if __name__ == "__main__":
    setup_kaggle()

    # Start health check server thread for Render Free Web Service
    threading.Thread(target=run_health_server, daemon=True).start()

    print("Starting Hermes Gateway on Render Cloud...")
    run_gateway(verbose=1, quiet=False, replace=True, force=True)
