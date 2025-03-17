FROM python:3.12-slim

# working directory
WORKDIR /app

# OS Dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Poetry
ENV PYTHONPATH=/app:$PYTHONPATH
RUN pip install poetry

# Install dependencies
RUN poetry install --no-root

# Cron job deployment
COPY cron/data-pipeline-cron /etc/cron.d/data-pipeline-cron
RUN echo >> /etc/cron.d/data-pipeline-cron
RUN chmod 0644 /etc/cron.d/data-pipeline-cron
RUN crontab /etc/cron.d/data-pipeline-cron
RUN touch /var/log/cron.log

# Run cron
CMD cron && tail -f /var/log/cron.log
