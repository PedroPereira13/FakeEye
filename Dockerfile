FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    git libssl-dev libffi-dev build-essential \
    python3-dev authbind && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -d /home/cowrie -s /bin/bash cowrie

RUN git clone https://github.com/cowrie/cowrie.git /home/cowrie/cowrie

WORKDIR /home/cowrie/cowrie

# Instala o cowrie como pacote (cria o comando 'cowrie' no PATH)
RUN pip install -e .

COPY --chown=cowrie:cowrie etc/cowrie.cfg /home/cowrie/cowrie/etc/cowrie.cfg

RUN chown -R cowrie:cowrie /home/cowrie/

USER cowrie

EXPOSE 2222

CMD ["cowrie", "start"]
