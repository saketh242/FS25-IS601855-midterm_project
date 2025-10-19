import logging
import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

log_dir = os.getenv('CALCULATOR_LOG_DIR', 'logs')
LOG_FILE = os.path.join(PROJECT_ROOT, log_dir, "calculator.log")


def log_operation(operation: str):
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, force=True)  # force to reconfigure
    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + operation)


def get_log():
    with open(LOG_FILE, "r") as file:
        return file.read()
