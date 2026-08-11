from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

LOG_PATH = "logs/web_access.log"
os.makedirs("logs", exist_ok=True)

# Credenciais "corretas" - ajuste conforme sua estratégia de honeypot
VALID_CREDENTIALS = {"admin": "admin123"}

def log_attempt(ip, username, password, success):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] IP={ip} user={username} pass={password} success={success}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    success = VALID_CREDENTIALS.get(username) == password

    log_attempt(ip, username, password, success)

    return jsonify({"success": success})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
