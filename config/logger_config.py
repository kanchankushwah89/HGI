import logging

# logger setup
logging.basicConfig(
    level=logging.INFO,  # Default logging level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

logger = logging.getLogger(__name__)  # Get a logger with the module's name