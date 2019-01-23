FROM python:3-slim

COPY requirements.txt /
RUN pip install --no-cache-dir -q -r /requirements.txt
COPY agent.py /

USER nobody
CMD while true; do /agent.py /config.yaml; sleep 60; done
