import shutil
import json
from pathlib import Path

from python_lib.file_utilities import FileUtilities

class ExampleDataCopier:
    def __init__(self, 
        logger, 
        file_utils: FileUtilities, 
        script_dir: Path, 
        hpc_root: Path, 
        copy_job_files: bool
    ):
        self.logger = logger
        self.file_utils = file_utils
        self.script_dir = script_dir
        self.hpc_root = hpc_root
        self.copy_job_files = copy_job_files
        

    def load_jobs_to_ignore(self, source_dir: Path):
        ignore_file = source_dir / "jobs_to_ignore.txt"
        if not ignore_file.exists():
            return set()
        
        try:
            with open(ignore_file, 'r', encoding='utf-8') as f:
                return set(line.strip() for line in f if line.strip())
        except Exception as e:
            self.logger.error(f"Failed to read {ignore_file}: {e}")
            return set()


    def run(self):
        source_dir = self.script_dir / "example_data"
        dest_jobs_dir = self.hpc_root / "ApsimWGP" / "jobs"
        apsim_files_dir = self.hpc_root / "ApsimFiles"
        apsim_files_dir_volume_path = "/hpc-root/ApsimFiles"

        if not source_dir.exists():
            self.logger.warning(f"Source job directory does not exist: {source_dir}")
            return

        self.file_utils.create_directory(dest_jobs_dir)
        self.file_utils.create_directory(apsim_files_dir)

        if self.copy_job_files:
            copied_json_files = self.copy_json_files(source_dir, dest_jobs_dir)
            for json_file in copied_json_files:
                self.update_path_in_file("ApsimPath", json_file, apsim_files_dir_volume_path)
        else:
            self.logger.info("Skipping copying of job JSON files as per user request.")

        self.copy_zip_files(source_dir, apsim_files_dir)
        self.copy_directories(source_dir, apsim_files_dir)


    def copy_json_files(self, source_dir: Path, dest_jobs_dir: Path):
        json_files = list(source_dir.glob("*.json"))
        if not json_files:
            self.logger.info(f"No JSON job files found in {source_dir}")
            return []

        ignored_jobs = self.load_jobs_to_ignore(source_dir)
        
        copied_files = []
        for file in json_files:
            if file.name in ignored_jobs:
                self.logger.info(f"Skipping {file.name} (listed in jobs_to_ignore.txt)")
                continue
            
            dest = dest_jobs_dir / file.name

            # The config file should be copied to the HPC Root Dir.
            if file.name == 'cgm_config.json':
                dest = self.hpc_root / file.name

            shutil.copy(file, dest)
            self.logger.info(f"Copied {file.name} to {dest}")
            copied_files.append(dest)
        return copied_files


    def update_path_in_file(
            self, 
            find_str: str,
            json_file: Path, 
            base_path: Path
        ):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if find_str in data:
                updated_path = str(base_path) + "/" + data[find_str]
                data[find_str] = updated_path

                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)

                self.logger.info(f"Updated '{find_str}' in {json_file} to {updated_path}")
        except Exception as e:
            self.logger.error(f"Failed to update {find_str} in {json_file}: {e}")


    def copy_directories(self, source_dir: Path, dest_dir: Path):
        directories = [item for item in source_dir.iterdir() if item.is_dir()]
        if not directories:
            self.logger.info(f"No directories found in {source_dir}")
            return

        for directory in directories:
            dest = dest_dir / directory.name
            shutil.copytree(directory, dest)
            self.logger.info(f"Copied directory {directory.name} to {dest}")


    def copy_zip_files(self, source_dir: Path, dest_dir: Path):
        zip_files = list(source_dir.glob("*.zip"))
        if not zip_files:
            self.logger.info(f"No ZIP files found in {source_dir}")
            return

        for file in zip_files:
            dest = dest_dir / file.name
            shutil.copy(file, dest)
            self.logger.info(f"Copied {file.name} to {dest}")
