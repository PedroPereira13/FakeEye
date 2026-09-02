"""
servidor_fakeeye.py

Servidor HTTP para o painel do FakeEye (honeypot).
- Serve os arquivos estaticos do dashboard (HTML, stats.json, etc.)
- Expoe o endpoint /comandos, que retorna os comandos executados
  por um IP especifico, extraidos dos logs do Cowrie.

Uso:
    python3 servidor_fakeeye.py
    -> abre em http://localhost:8002/
"""

import re
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory

# ---------------------------------------------------------------------------
# Configuracao
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"     # onde ficam os ssh_YYYYMMDD.log do Cowrie
LOG_PATTERN = "ssh_*.log"       # pega todos os arquivos de log disponiveis
DASHBOARD_DIR = BASE_DIR        # onde estao dashboard_teste.html e stats.json
LIMITE_PADRAO = 20

app = Flask(__name__, static_folder=str(DASHBOARD_DIR), static_url_path="")

# Extrai "CMD: <comando>" e a data ISO (formato padrao dos logs do Cowrie)
RE_CMD = re.compile(r"CMD:\s*(.+)")
RE_DATA = re.compile(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})")


def ip_pattern(ip: str) -> re.Pattern:
    """
    Regex que casa o IP como token isolado, evitando falso positivo
    de substring (ex: '1.2.3.4' dentro de '21.2.3.44').
    """
    return re.compile(r"(?<![\d.])" + re.escape(ip) + r"(?![\d.])")


def listar_arquivos_log():
    """Retorna todos os arquivos de log encontrados, em ordem cronologica."""
    if not LOG_DIR.exists():
        return []
    return sorted(LOG_DIR.glob(LOG_PATTERN))


@app.route("/comandos")
def get_comandos():
    ip = request.args.get("ip", "").strip()
    if not ip:
        return jsonify({"erro": "IP nao informado"}), 400

    try:
        limite = int(request.args.get("limite", LIMITE_PADRAO))
    except ValueError:
        limite = LIMITE_PADRAO

    arquivos = listar_arquivos_log()
    if not arquivos:
        return jsonify({"erro": f"Nenhum log encontrado em {LOG_DIR}"}), 404

    padrao_ip = ip_pattern(ip)
    comandos = []

    for caminho in arquivos:
        try:
            with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                for linha in f:
                    if not padrao_ip.search(linha):
                        continue
                    cmd_match = RE_CMD.search(linha)
                    if not cmd_match:
                        continue
                    data_match = RE_DATA.search(linha)
                    comandos.append({
                        "data": data_match.group(1) if data_match else "N/A",
                        "comando": cmd_match.group(1).strip(),
                        "arquivo": caminho.name,
                    })
        except OSError:
            # nao deixa um arquivo problematico derrubar a resposta inteira
            continue

    total_encontrado = len(comandos)
    comandos_recentes = comandos[-limite:] if limite > 0 else comandos

    return jsonify({
        "ip": ip,
        "total_comandos": total_encontrado,
        "comandos": comandos_recentes,
    })


@app.route("/")
def index():
   return send_from_directory(str(DASHBOARD_DIR), "dashboard.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
