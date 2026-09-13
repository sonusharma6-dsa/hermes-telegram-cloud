import os
import sys
import time
import shutil
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

    # Clear cached auth.json to remove stale 429/exhausted locks
    auth_json_path = os.path.join(config_dir, "auth.json")
    if os.path.exists(auth_json_path):
        os.remove(auth_json_path)
        print("Cleared stale auth.json cache.")

    # Ensure GEMINI_API_KEY environment variable is populated
    google_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if google_key:
        os.environ["GOOGLE_API_KEY"] = google_key
        os.environ["GEMINI_API_KEY"] = google_key

    # Write config.yaml enabling stable gemini-flash-latest with 1,500 RPD quota
    config_path = os.path.join(config_dir, "config.yaml")
    config_content = """model:
  default: gemini-flash-latest
  provider: gemini
agent:
  max_turns: 120
  verbose: false
  reasoning_effort: none
memory:
  memory_enabled: true
  user_profile_enabled: true
  nudge_interval: 5
session_reset:
  mode: idle
  idle_minutes: 10080
group_sessions_per_user: true
display:
  show_reasoning: false
platform_toolsets:
  cli:
    - browser
    - clarify
    - code_execution
    - computer_use
    - cronjob
    - delegation
    - file
    - memory
    - session_search
    - skills
    - terminal
    - todo
    - vision
    - web
  telegram:
    - browser
    - clarify
    - code_execution
    - computer_use
    - cronjob
    - delegation
    - file
    - memory
    - session_search
    - skills
    - terminal
    - todo
    - vision
    - web
platforms:
  telegram:
    enabled: true
"""
    with open(config_path, "w") as f:
        f.write(config_content)
    print("Configured ~/.hermes/config.yaml")

    # Create SOUL.md to retain core context across container redeploys
    soul_path = os.path.join(config_dir, "SOUL.md")
    soul_content = """# Permanent Bot Memory & Context
- User Name: Sonu Sharma (@sonusharma6-dsa)
- Primary Mission: Autonomous AI Assistant, GSoC Open-Source Contributor, SatQuery AI, StorySparkAI, and Hackathon Co-pilot (@sonu_hermes_ai_bot).
- GitHub Account: sonusharma6-dsa
- Capabilities: Web Search, Browse Websites, Search GSoC issues, fork repos, write code fixes, run test suites, commit changes, and submit PRs on GitHub.
"""
    with open(soul_path, "w") as f:
        f.write(soul_content)
    print("Configured ~/.hermes/SOUL.md")

    # Copy repository skills to ~/.hermes/skills/
    local_skills_dir = os.path.join(os.path.dirname(__file__), "skills")
    target_skills_dir = os.path.join(config_dir, "skills")
    if os.path.exists(local_skills_dir):
        os.makedirs(target_skills_dir, exist_ok=True)
        for item in os.listdir(local_skills_dir):
            s_src = os.path.join(local_skills_dir, item)
            s_dst = os.path.join(target_skills_dir, item)
            if os.path.isdir(s_src):
                shutil.copytree(s_src, s_dst, dirs_exist_ok=True)
        print("Copied custom skills to ~/.hermes/skills/")

    # Write .env file in ~/.hermes if environment variables exist
    env_path = os.path.join(config_dir, ".env")
    env_vars = ["OPENROUTER_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY", "TELEGRAM_BOT_TOKEN", "TELEGRAM_ALLOWED_USERS", "KAGGLE_API_TOKEN", "GH_TOKEN", "GITHUB_TOKEN"]
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
