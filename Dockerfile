# Use Python base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (including PostgreSQL client and cron)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copy the project files
COPY . .

# Set the PYTHONPATH environment variable so Python can find the config module
ENV PYTHONPATH=/app:$PYTHONPATH

# Install Poetry
RUN pip install poetry

# Install dependencies using Poetry
RUN poetry install --no-root

# Copy the cron job file into the container
COPY cron/data-pipeline-cron /etc/cron.d/data-pipeline-cron

# Ensure newline is at the end of the cron file (fix for missing newline error)
RUN echo >> /etc/cron.d/data-pipeline-cron

# Set the correct permissions for the cron job file
RUN chmod 0644 /etc/cron.d/data-pipeline-cron

# Apply the cron job to crontab
RUN crontab /etc/cron.d/data-pipeline-cron

# Create a log file for cron (optional, for debugging)
RUN touch /var/log/cron.log

# Copy the shell script that starts the pipeline and cron
COPY scripts/start.sh /start.sh

# Give execute permissions to the start script
RUN chmod +x /start.sh

# Run the shell script to execute `main.py` immediately and then start cron
CMD ["/start.sh"]
