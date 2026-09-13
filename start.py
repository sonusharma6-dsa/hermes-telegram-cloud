import os
import sys
import time
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from hermes_cli.gateway import run_gateway

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Hermes Telegram Gateway is Live & Awake!")

    def log_message(self, format, *args):
        pass  # Silence HTTP access logs

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"Render Health Server listening on port {port}...")
    server.serve_forever()

def keep_alive_pinger():
    """
    Self-pings every 5 minutes to prevent Render Free Tier from spinning down to sleep!
    """
    time.sleep(10)  # Wait for server startup
    url = os.environ.get("RENDER_EXTERNAL_URL", "https://hermes-telegram-cloud-5ry0.onrender.com")
    print(f"Self-ping keep-alive loop started targeting: {url}")
    
    while True:
        try:
            resp = requests.get(url, timeout=15)
            print(f"[Keep-Alive] Self ping success: HTTP {resp.status_code}")
        except Exception as err:
            print(f"[Keep-Alive] Ping error: {err}")
        time.sleep(300)  # Ping every 5 minutes

def setup_hermes_config():
    config_dir = os.path.expanduser("~/.hermes")
    os.makedirs(config_dir, exist_ok=True)

    # Write config.yaml to enforce OpenRouter auto model and disable reasoning effort (prevents 400 & 429 gateway errors)
    config_path = os.path.join(config_dir, "config.yaml")
    config_content = """model:
  default: openrouter/auto
  provider: openrouter
agent:
  max_turns: 120
  verbose: false
  reasoning_effort: none
display:
  show_reasoning: false
"""
    with open(config_path, "w") as f:
        f.write(config_content)
    print("Configured ~/.hermes/config.yaml")

    # Write .env file in ~/.hermes if environment variables exist
    env_path = os.path.join(config_dir, ".env")
    env_vars = ["OPENROUTER_API_KEY", "GOOGLE_API_KEY", "TELEGRAM_BOT_TOKEN", "TELEGRAM_ALLOWED_USERS", "KAGGLE_API_TOKEN"]
    env_lines = []
    for var in env_vars:
        val = os.environ.get(var)
        if val:
            env_lines.append(f"{var}={val}")

    if env_lines:
        with open(env_path, "w") as f:
            f.write("\n".join(env_lines) + "\n")
        print("Configured ~/.hermes/.env")

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
    setup_hermes_config()
    setup_kaggle()

    # Start health check server thread for Render Free Web Service
    threading.Thread(target=run_health_server, daemon=True).start()

    # Start Keep-Alive self-pinger thread (prevents Render sleep)
    threading.Thread(target=keep_alive_pinger, daemon=True).start()

    print("Starting Hermes Gateway on Render Cloud...")
    run_gateway(verbose=1, quiet=False, replace=True, force=True)
