import shutil
import logging
from pathlib import Path

class FileUtilities:
    def __init__(self, logger: logging.Logger):
        self.logger = logger


    def create_directory(self, path: Path):
        if not path.exists():
            self.logger.info(f'Creating folder at "{path}"')
            path.mkdir(parents=True, exist_ok=True)


    def delete_directory(self, path: Path):
        if path.exists() and path.is_dir():
            self.logger.info(f'Deleting existing {path} directory and all contents...')
            shutil.rmtree(path)


    def generate_env_file(self, path: Path):
        self.logger.info(f'Generating .env file at "{path}"')
        with path.open("w") as f:
            f.write("RELAY_IP_FILE=/relay-volume/relay_ip.txt\n")
            f.write("HPC_ROOT=/hpc-root\n")
            f.write("RSTUDIO_PASSWORD=changeyourpasshere\n")
