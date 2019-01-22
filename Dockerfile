FROM python:3-slim

COPY agent.py requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

USER nobody
CMD while true; do /agent.py /config.yaml; sleep 60; done
