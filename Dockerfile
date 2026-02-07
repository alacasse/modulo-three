FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY modulo_three/ modulo_three/

RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "-m", "modulo_three"]
