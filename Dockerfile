FROM python:3.11-slim as builder

WORKDIR /app

RUN pip install --no-cache-dir poetry

ENV POETRY_VENV_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root


FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local /usr/local

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "src.testastrom.main:app", "--host", "0.0.0.0", "--port", "8000"]