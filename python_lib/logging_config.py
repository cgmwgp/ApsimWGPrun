import logging
import sys
from pathlib import Path

class LoggerSetup:
    def __init__(self, log_file: Path):
        self.log_file = log_file


    def setup_logger(self, name: str = "docker_compose_launcher") -> logging.Logger:
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("[%(levelname)s] %(message)s")

        if not logger.handlers:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            file_handler = logging.FileHandler(self.log_file, mode='w')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger
