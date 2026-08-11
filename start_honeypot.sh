#!/bin/bash
cd /home/pedro/FakeEye
source venv/bin/activate
docker-compose up -d
nohup python web_server.py > logs/web_server.log 2>&1 &
echo "Honeypot iniciado!"
