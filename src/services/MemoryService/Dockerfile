FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y curl && \
    pip install poetry && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

ENV POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /build

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

WORKDIR /service

COPY src/services/MemoryService/app /service/app
COPY src/services/MemoryService/entrypoint.sh /service/
COPY src/services/MemoryService/alembic.ini /service/

RUN chmod +x /service/entrypoint.sh && \
    chown -R appuser:appuser /service

USER appuser

ENTRYPOINT ["/service/entrypoint.sh"]