FROM python:3.10-slim AS builder

RUN pip install --no-cache-dir Pyro5

EXPOSE 9090

CMD ["pyro5-ns", "--host", "0.0.0.0", "--port", "9090"]
