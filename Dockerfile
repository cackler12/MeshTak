FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Configure uv
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/app/.venv
ENV PYTHONUNBUFFERED=1

# Copy dependency metadata first
COPY pyproject.toml uv.lock ./

# Install dependencies without installing the project yet
RUN uv sync --frozen --no-install-project

# Copy application source
COPY src/ ./src/
COPY certs/ ./certs
COPY README.md README.md

# Install the project itself
RUN uv sync --frozen

# Run the configured project entry point
CMD ["/app/.venv/bin/meshtak"]