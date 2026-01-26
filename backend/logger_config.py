# backend/logger_config.py

import logging
import os

# File logs
LOG_DIR = "backend/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Root log
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Basic logger
logging.basicConfig(
    level=logging.INFO,  # Nivel mínimo de log: INFO, WARNING, ERROR
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # Guarda en archivo
        logging.StreamHandler()          # También muestra por consola
    ]
)

# Logger Nombre Looping
logger = logging.getLogger("looping_logger")
