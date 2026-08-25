#!/usr/bin/env python3
import json
import re
import os
from collections import Counter
from datetime import datetime

pasta_logs = 'logs/'

if not os.path.exists(pasta_logs):
    print(f"Pasta nao encontrada: {pasta_logs}")
    exit(1)

ips_por_ataque = Counter()
credenciais = Counter()
ataques_por_dia = Counter()
ataques_por_hora = Counter()
total_ataques = 0
sucessos = 0
falhas = 0
ips_vistos = set()

arquivos = os.listdir(pasta_logs)
arquivos_log = [f for f in arquivos if f.startswith('ssh_') and f.endswith('.log')]

for arquivo in arquivos_log:
    caminho = os.path.join(pasta_logs, arquivo)
    with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
        for linha in f:
            if 'login attempt' in linha:
                total_ataques += 1
                
                # Extrair IP (formato: [ssh,id,IP])
                #ip_match = re.search(r'\] (\d+\.\d+\.\d+\.\d+)', linha)
                ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', linha)
                if ip_match:
                    ip = ip_match.group(1)
                    ips_vistos.add(ip)
                    ips_por_ataque[ip] += 1
                
                # Extrair data
                data_match = re.search(r'(\d{4}-\d{2}-\d{2})', linha)
                if data_match:
                    data = data_match.group(1)
                    ataques_por_dia[data] += 1
                
                # Extrair hora
                hora_match = re.search(r'T(\d{2}):', linha)
                if hora_match:
                    hora = hora_match.group(1)
                    ataques_por_hora[hora] += 1
                
                # Extrair credencial
                cred_match = re.search(r'login attempt \[([^/]+)/([^\]]+)\]', linha)
                if cred_match:
                    usuario = cred_match.group(1)
                    senha = cred_match.group(2)
                    credenciais[f"{usuario}/{senha}"] += 1
                
                if 'succeeded' in linha:
                    sucessos += 1
                else:
                    falhas += 1

ataques_por_hora_completo = {f"{h:02d}": ataques_por_hora.get(f"{h:02d}", 0) for h in range(24)}

resultado = {
    "total_ataques": total_ataques,
    "ips_unicos": len(ips_vistos),
    "sucessos": sucessos,
    "falhas": falhas,
    "top_ips": dict(ips_por_ataque.most_common(10)),
    "top_credenciais": dict(credenciais.most_common(10)),
    "ataques_por_dia": dict(sorted(ataques_por_dia.items())),
    "ataques_por_hora": ataques_por_hora_completo,
    "ultima_atualizacao": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

with open('stats.json', 'w') as f:
    json.dump(resultado, f, indent=2)

print(f"Stats gerado com {total_ataques} ataques de {len(arquivos_log)} arquivos")
print(f"IPs unicos encontrados: {len(ips_vistos)}")
