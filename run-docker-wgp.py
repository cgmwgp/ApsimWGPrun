import sys
import argparse
from pathlib import Path

from python_lib.logging_config import LoggerSetup
from python_lib.file_utilities import FileUtilities
from python_lib.docker_compose_runner import DockerComposeRunner
from python_lib.example_data_copier import ExampleDataCopier


def parse_args():
    parser = argparse.ArgumentParser(description="Launch Docker Compose with environment setup.")
    parser.add_argument(
        "compose_file",
        type=Path,
        help="Path to the docker-compose YAML file to use",
        default=Path("docker-compose-wgp-images.yml")
    )
    return parser.parse_args()


def main():
    try:
        logger = LoggerSetup(Path("logs/setup.log")).setup_logger()
        file_utils = FileUtilities(logger)
        args = parse_args()
        copy_job_files = True

        if not args.compose_file.exists():
            logger.error(f"Docker Compose file not found: {args.compose_file}")
            sys.exit(1)

        script_dir = Path(__file__).resolve().parent
        hpc_root = script_dir / "hpc-root"
        relay_volume = script_dir / "relay-volume"
        env_file = script_dir / ".env"

        file_utils.delete_directory(hpc_root)
        file_utils.create_directory(hpc_root)

        ExampleDataCopier(logger, file_utils, script_dir, hpc_root, copy_job_files).run()

        file_utils.delete_directory(relay_volume)
        file_utils.create_directory(relay_volume)
        file_utils.generate_env_file(env_file)

        DockerComposeRunner(logger, script_dir, args.compose_file).run()

    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
