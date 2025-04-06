import logging
from logging.handlers import RotatingFileHandler
import os

log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, "sync.log")
logger = logging.getLogger("gorilla_logger")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)