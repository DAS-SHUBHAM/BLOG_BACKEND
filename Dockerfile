FROM ghcr.io/astral-sh/uv:python3.11-alpine

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock ./

# Installs using the container's native Python 3.11 matching the updated pyproject.toml
RUN uv sync --frozen --no-dev --no-install-project

COPY ./app /app/app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]                                                                                                                                   