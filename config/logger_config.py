# logger_config.py
import logging

# Set up the logger
logging.basicConfig(
    level=logging.INFO,  # Default logging level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

logger = logging.getLogger(__name__)  # Get a logger with the module's name