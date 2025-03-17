# dev.Dockerfile
FROM python:3.12

# Install system dependencies needed to install Poetry
RUN apt-get update && apt-get install -y curl

# Install Poetry (official installation script)
# https://python-poetry.org/docs/#installation
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Set a working directory
WORKDIR /app

# Copy dependency files first
# COPY pyproject.toml poetry.lock README.md ./
COPY . .

# Install dependencies (including dev dependencies)
RUN poetry install

# Copy the rest of the source code
# COPY . .

# Expose port 8000 for convenience (optional)
EXPOSE 8000