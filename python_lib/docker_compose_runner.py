import os
import subprocess
import sys
from pathlib import Path

class DockerComposeRunner:
    def __init__(self, logger, script_dir: Path, compose_file: Path):
        self.logger = logger
        self.script_dir = script_dir
        self.compose_file = compose_file

    def down(self):
        self.logger.info("Stopping and removing any existing Docker containers with docker-compose down...")
        os.chdir(self.script_dir)
        down_cmd = [
            "docker-compose",
            "-f", str(self.compose_file),
            "--env-file", ".env",
            "down"
        ]
        self.logger.info("Running command: %s", " ".join(down_cmd))
        try:
            subprocess.run(down_cmd, check=True)
            self.logger.info("docker-compose down completed successfully.")
        except subprocess.CalledProcessError as e:
            self.logger.warning("docker-compose down failed with exit code %s, continuing...", e.returncode)

    def up(self):
        self.logger.info("Starting docker-compose up...")
        os.chdir(self.script_dir)
        up_cmd = [
            "docker-compose",
            "-f", str(self.compose_file),
            "--env-file", ".env",
            "up",
            "--build"
        ]
        self.logger.info("Running command: %s", " ".join(up_cmd))
        try:
            subprocess.run(up_cmd, check=True)
            self.logger.info("docker-compose up completed successfully.")
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user. Shutting down Docker Compose...")
            self.down()
            raise
        except subprocess.CalledProcessError as e:
            self.logger.error("docker-compose up failed with exit code %s", e.returncode)
            sys.exit(e.returncode)

    def run(self):
        self.logger.info("Executing DockerComposeRunner.run()...")
        self.down()
        self.up()
