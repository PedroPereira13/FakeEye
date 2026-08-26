# FakeEye - Honeypot para Câmeras IP e Dispositivos IoT

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Docker](https://img.shields.io/badge/docker-✓-blue)
![AWS](https://img.shields.io/badge/AWS-EC2-orange)

**Trabalho de Conclusão de Curso (TCC)**
**Etec Polivalente de Americana - Extensão Fatec**
**Curso: Análise e Desenvolvimento de Sistemas (AMS/DS)**

---

## Sobre o Projeto

O **FakeEye** é um honeypot de baixa interação desenvolvido para simular câmeras IP e dispositivos IoT, com o objetivo de coletar dados sobre ataques cibernéticos e comportamentos de invasores.

O projeto é inspirado no artigo acadêmico **"SweetCam" (DOI: 10.1145/3605758.3623495)** e utiliza o **Cowrie** como base para emulação de serviços SSH.

### Objetivos

* Simular uma câmera IP HiVision de forma realista
* Coletar tentativas de login SSH e comandos executados por atacantes
* Registrar tentativas de login na interface web
* Gerar gráficos e análises a partir dos dados coletados
* Fornecer material para análise de ameaças e inteligência de segurança

---

## Tecnologias Utilizadas

| Tecnologia                  | Finalidade                                       |
| --------------------------- | ------------------------------------------------ |
| **Docker / Docker Compose** | Containerização e orquestração dos serviços      |
| **Cowrie**                  | Honeypot SSH/Telnet para emulação de sistema IoT |
| **Python / Flask**          | Servidor web para interface da câmera IP         |
| **AWS EC2**                 | Hospedagem na nuvem 24/7                         |
| **HTML / CSS / JavaScript** | Interface visual da câmera HiVision              |
| **Chart.js**                | Gráficos interativos no dashboard                |
| **Git / GitHub**            | Versionamento de código                          |

---

## Arquitetura do Sistema

```text
┌─────────────────────────────────────────────────────────────────┐
│                         FAKEEYE HONEYPOT                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐       ┌─────────────────────────────────┐  │
│  │   COWRIE SSH    │       │      INTERFACE WEB (Flask)     │  │
│  │    (Porta 22)   │       │          (Porta 80)             │  │
│  └────────┬────────┘       └──────────────┬──────────────────┘  │
│           │                               │                     │
│           └───────────────┬───────────────┘                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                SISTEMA DE ARQUIVOS VIRTUAL              │   │
│  │                                                         │   │
│  │  - /etc/passwd              (usuários falsos)            │   │
│  │  - /etc/version             (firmware da câmera)        │   │
│  │  - /var/log/camera.log      (logs falsos)               │   │
│  │  - /root/.bash_history      (histórico falso)            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  LOGS E MONITORAMENTO                   │   │
│  │                                                         │   │
│  │  - web_access.log      (tentativas de login web)        │   │
│  │  - logs do Cowrie      (tentativas SSH)                 │   │
│  │  - Dashboard           (gráficos e análises)            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```


## Instalação e Execução

### Pré-requisitos

* Docker e Docker Compose
* Python 3.11+
* Git
* AWS EC2 para produção

### 1. Clonar o repositório

```bash
git clone https://github.com/PedroPereira13/FakeEye.git
cd FakeEye
```

### 2. Subir o container do Cowrie

```bash
docker-compose up -d
```

### 3. Subir a interface web

```bash
source venv/bin/activate
sudo nohup $(which python3) web_server.py > logs/web_server.log 2>&1 &
```

### 4. Verificar se está rodando

```bash
docker ps
ps aux | grep web_server.py
```

### 5. Acessar a interface web

* Local: `http://localhost`
* Credenciais padrão: `admin/admin123`

---

## Dashboard de Análise

O projeto inclui um dashboard interativo para visualização dos ataques coletados.

### Gráficos disponíveis

* **Top 10 IPs atacantes**
* **Top 10 credenciais testadas**
* **Evolução dos ataques por dia**
* **Distribuição de ataques por hora**
* **Taxa de sucesso vs. falha**

### Gerar dados para o dashboard

```bash
python3 gerar_stats_fakeeye.py
```

### Acessar o dashboard

```bash
python3 -m http.server 8000
```

No navegador:

```text
http://localhost:8000/dashboard_teste.html
```

---

## Estrutura do Projeto

```text
FakeEye/
├── docker-compose.yml      # Orquestração dos containers
├── Dockerfile              # Build do container Cowrie
├── web_server.py           # Servidor Flask da interface web
├── start_honeypot.sh       # Script de inicialização automática
├── dashboard_teste.html    # Dashboard com gráficos
├── gerar_stats_fakeeye.py  # Script para gerar stats.json
├── templates/
│   └── index.html          # Interface da câmera
├── honeyfs/                # Sistema de arquivos falso
│   ├── etc/
│   │   ├── passwd          # Usuários falsos
│   │   ├── version         # Firmware da câmera
│   │   ├── issue           # Banner de login
│   │   └── camera.conf     # Configurações falsas
│   ├── var/
│   │   └── log/
│   │       └── camera.log  # Logs falsos da câmera
│   └── root/
│       └── .bash_history   # Histórico de comandos falso
├── logs/
│   ├── web_access.log      # Tentativas de login web
│   ├── web_server.log      # Logs do servidor Flask
│   └── ssh_*.log           # Logs do Cowrie
└── data/                   # Dados do Cowrie
```

---

## Comandos Úteis

### Ver logs

#### Logs do honeypot

```bash
docker-compose logs -f
```

#### Tentativas de login

```bash
docker-compose logs | grep "login attempt"
```

#### Comandos executados

```bash
docker-compose logs | grep "CMD:"
```

#### Logs da interface web

```bash
tail -f logs/web_access.log
```

---

## Salvar Logs

### Salvar logs do SSH

```bash
docker-compose logs > logs/ssh_$(date +%Y%m%d).log
```

### Ver logs da interface web

```bash
cat logs/web_access.log
```

---

## Manutenção

### Parar o honeypot

```bash
docker-compose down
```

### Reiniciar o honeypot

```bash
docker-compose up -d
```

### Verificar status

```bash
docker ps
```

---

## Segurança

* O honeypot roda em **container Docker** isolado.
* A **porta 22** é disponibilizada para o honeypot para permitir a coleta de tentativas de ataque.
* O firewall é configurado na AWS.
* Os logs são armazenados separadamente.
* O ambiente foi desenvolvido com finalidade acadêmica e de pesquisa em segurança da informação.

---

## Referências

* **SweetCam: Honeypot para câmeras IP**
  DOI: [https://doi.org/10.1145/3605758.3623495](https://doi.org/10.1145/3605758.3623495)

* **Cowrie SSH/Telnet Honeypot**
  [https://github.com/cowrie/cowrie](https://github.com/cowrie/cowrie)

* **Docker**
  [https://www.docker.com/](https://www.docker.com/)

* **AWS EC2**
  [https://aws.amazon.com/ec2/](https://aws.amazon.com/ec2/)

---

## Autor

* **Pedro Pereira**
* **Edgar Santori**
* **Lucca Faria**
* **Raphael Eduardo**


* Projeto: [https://github.com/PedroPereira13/FakeEye](https://github.com/PedroPereira13/FakeEye)

---

## Licença

Este projeto é de uso acadêmico para fins de pesquisa em segurança da informação.

---

## Status do Projeto

* [x] Honeypot SSH rodando 24/7 na AWS
* [x] Interface web funcional
* [x] Dashboard com gráficos em tempo real
* [x] Coleta de dados ativa
* [x] Documentação em andamento

---

**Última atualização:** Agosto de 2026
