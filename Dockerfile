FROM python:latest AS base

WORKDIR /app

ENV POETRY_HOME=/opt/poetry
ENV PATH=$POETRY_HOME/bin:$PATH
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-root --without dev


FROM python:latest

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=base --chown=appuser:appuser /app/.venv ./.venv
COPY --chown=appuser:appuser . .

RUN adduser --system --group --no-create-home appuser
USER appuser

CMD ["python", "-m", "uvicorn", "--factory", "app.app:create_app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]