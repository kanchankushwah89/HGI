#!/bin/bash

# Run the pipeline immediately (first execution of main.py)
echo "Running pipeline immediately..."
poetry run python /app/pipeline/main.py

# Start the cron daemon (subsequent hourly executions)
echo "Starting cron..."
cron -f
