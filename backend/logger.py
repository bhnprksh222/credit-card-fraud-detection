import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logging
logger = logging.getLogger("chatapp")
logger.setLevel(logging.DEBUG)

# Log format
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Console Handler (prints logs to the terminal)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)

# File Handler (stores logs in a rotating file)
file_handler = RotatingFileHandler(
    "logs/chatapp.log", maxBytes=5 * 1024 * 1024, backupCount=3
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
