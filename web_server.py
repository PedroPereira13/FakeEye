from flask import Flask, render_template, request, jsonify, make_response
from datetime import datetime
import os
import time
import random

app = Flask(__name__)

LOG_PATH = "logs/web_access.log"
os.makedirs("logs", exist_ok=True)

VALID_CREDENTIALS = {"admin": "admin123"}

FIRMWARE_BANNER = "HiVision-Embedded-Httpd/2.3"  # nome fictício, mas plausível para dispositivo embarcado


def log_attempt(ip, username, password, success, user_agent=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] IP={ip} user={username} pass={password} success={success} ua=\"{user_agent}\"\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)


@app.after_request
def set_device_headers(response):
    """
    Substitui/adiciona headers para parecer um servidor HTTP
    embarcado real, em vez do Werkzeug de desenvolvimento padrão.
    Isso é aplicado a TODAS as respostas.
    """
    response.headers["Server"] = FIRMWARE_BANNER
    # Remove headers que entregam "é Flask/Werkzeug"
    response.headers.pop("X-Powered-By", None)
    return response


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "")
   
    time.sleep(random.uniform(0.2, 0.6))

    success = VALID_CREDENTIALS.get(username) == password

    log_attempt(ip, username, password, success, user_agent)

    return jsonify({"success": success})


if __name__ == "__main__":
  
    app.run(host="0.0.0.0", port=80, threaded=True)
