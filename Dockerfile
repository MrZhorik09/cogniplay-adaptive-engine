# syntax=docker/dockerfile:1

# --- Base image -------------------------------------------------------------
# Slim variant keeps the image small; matches the oldest Python version
# supported by the project (see pyproject.toml: requires-python = ">=3.9").
FROM python:3.11-slim AS base

# Prevent Python from writing .pyc files and buffer stdout/stderr so logs
# show up immediately in `docker logs` / CI output.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# --- Dependencies -------------------------------------------------------------
# Copy only dependency manifests first so Docker can cache this layer and
# skip reinstalling dependencies when only application code changes.
COPY pyproject.toml requirements.txt requirements-dev.txt ./
COPY src ./src

RUN pip install --upgrade pip && \
    pip install .

# --- Application --------------------------------------------------------------
COPY data ./data
COPY tests ./tests

# Run as a non-root user (good practice for containers that may run in a
# shared cluster, and required by some CI/CD security scanners).
RUN useradd --create-home --uid 1000 appuser
USER appuser

# The engine is a CLI, not a long-running server, so there is no EXPOSE/port.
# Default command: print CLI help. Override at `docker run` time, e.g.:
#   docker run adaptive-engine simulate --items data/sample_item_bank.csv \
#       --true-theta 1.2 --rounds 30 --seed 7
ENTRYPOINT ["python", "-m", "adaptive_engine.cli"]
CMD ["--help"]
