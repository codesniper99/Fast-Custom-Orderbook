import time
from enum import Enum

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"

class Log:
    def __init__(self, log_file):
        self.log_file = log_file

    def log(self, level, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} [{level}] {message}\n"
        with open(self.log_file, "a") as f:
            f.write(log_entry)

    def info(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} [{LogLevel.INFO}] {message}\n"
        with open(self.log_file, "a") as f:
            f.write(log_entry)
