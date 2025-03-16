# Use Python base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (including PostgreSQL client)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the project files
COPY . .

# Install Poetry
RUN pip install poetry

# Install dependencies using Poetry
RUN poetry install --no-root

# Entry point to run the pipeline
CMD ["poetry", "run", "python", "pipeline/pipeline.py"]
