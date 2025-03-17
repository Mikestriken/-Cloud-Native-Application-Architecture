# prod.Dockerfile
FROM python:3.12-slim
# Create a non-root user for security
RUN useradd -m myuser

# Switch to the new user
USER myuser

# Set the working directory
WORKDIR /app

# Temporarily become root to install system dependencies
USER root
RUN apt-get update && apt-get install -y curl

# Switch back to non-root user
USER myuser

# Install Poetry
# See https://python-poetry.org/docs/#installation
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/home/myuser/.local/bin:$PATH"

# Copy dependency files and install dependencies
# COPY --chown=myuser:myuser pyproject.toml poetry.lock /app/
COPY --chown=myuser:myuser . /app
RUN poetry install --no-interaction --no-ansi

# Copy the remaining application files
# COPY --chown=myuser:myuser . /app

# Expose port 8000 for FastAPI
EXPOSE 8000

# Start the FastAPI server with Uvicorn
CMD ["poetry", "run", "uvicorn", "fastapi_lab.main:app", "--host", "0.0.0.0", "--port", "8000"]