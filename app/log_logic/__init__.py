import os
import logging

from datetime import datetime

# Get the project root directory (go up from app/log_logic to the project root)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_FILE = os.path.join(PROJECT_ROOT, 'logs', 'calculator.log')

def log_operation(operation: str):
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + operation)

def get_log():
    with open(LOG_FILE, 'r') as file:
        return file.read()