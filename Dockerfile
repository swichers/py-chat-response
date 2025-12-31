FROM python:3.13-slim AS build

ENV POETRY_VERSION=2.2.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

WORKDIR $PYSETUP_PATH

COPY poetry.lock pyproject.toml LICENSE.txt ./

RUN poetry install --only main --no-root --no-ansi

FROM python:3.13-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    VENV_PATH="/opt/pysetup/.venv" \
    PATH="/opt/pysetup/.venv/bin:$PATH"

RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m -d /home/appuser -s /bin/bash appuser

WORKDIR /app

COPY --from=build --chown=appuser:appgroup /opt/pysetup/.venv /opt/pysetup/.venv
COPY --chown=appuser:appgroup main.py main.py
COPY --chown=appuser:appgroup src src
COPY --chown=appuser:appgroup contexts/default.md contexts/default.md
RUN chmod 444 contexts/default.md

USER appuser

EXPOSE 8001

ENTRYPOINT ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]