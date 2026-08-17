# Docker Compose Launcher for CGM Platform

This Python script sets up a self-contained environment, and launches a suite of CGM-related Docker containers using `docker-compose`. It prepares input data, sets up necessary volumes, and manages container start-up and shutdown automatically.

---

## ✅ What It Does

1. **Cleans and sets up directories:**
   - Deletes and recreates the following directories that are also mounted as volumes in Docker: 
      - `hpc-root/`
      - `relay-volume/`
   - Creates a `.env` file with required environment variables

2. **Copies example input data:**
   - JSON job files and folders from `example_data/` to `hpc-root/ApsimWGP/jobs/`
   - ZIP files into `hpc-root/ApsimFiles/` - These should be zipped up Apsim Files including their corresponding weather data.
   - Updates `ApsimPath` fields in JSON files to the appropriate in-container volume path
   - Skips any JSON files listed in `example_data/jobs_to_ignore.txt` (one filename per line)

3. **Starts the following Docker services:**
   - `CGMRelay`
   - `CGMClient (x5)`
   - `ApsimWGP`


---

## 📁 Folder Structure

Expected structure:

```
project-root/
├── example_data/
│   ├── Dataset1.json - This is the ApsimWGP Job (json format).
│   ├── DataSet1/ - These are the input files for ApsimWGP.
│   └── ApsimDS1.zip - This is the APSIM file and its corresponding weather files.
├── docker-compose-wgp-images.yml
├── run-docker-wgp.py
└── README.md
```

- `example_data/`: Contains input job JSON files, ZIP files, and any required directories.
- `docker-compose-wgp-images.yml`: Defines the services to be started.
- `run-docker-wgp.py`: The main script to set everything up and run the containers.
- `README.md`: You're reading it.

This can be modified to suit your needs.

---

## 🚀 How to Run

1. Ensure Docker and Docker Compose are installed.
2. Run the launcher script like this:

```bash
python run-docker-wgp.py docker-compose-wgp-images.yml
```

The Python script will handle running docker compose up and down. For example, it will run: 

Up command: 

```bash
docker-compose -f docker-compose-wgp-images.yml --env-file .env up --build
```

Down command: 

```bash
docker-compose -f docker-compose-wgp-images.yml --env-file .env down
```

---

## 🪵 Logging

- The script logs are printed to the console **and** saved to:  
  ```
  logs/setup.log
  ```
- The Application logs are printed to the console **and** saved to: 
  ```
  hpc-root/file_logs/  
  ```
  These logs are written by the applications listed in the Docker Services above.

---

## ⚠️ Notes

- If `example_data/` is missing or empty, the script logs a warning and continues.
- The script will stop and log an error if the specified `docker-compose.yml` file does not exist.
- If `docker-compose up` fails, the script exits with the appropriate error code.

---

## 🔧 Customization Tips

- To skip copying job JSONs, modify the `copy_job_files` flag in `main()`.
- To add more services or modify volumes, update your `docker-compose_x.yml` accordingly.

---

## 🛠️ Troubleshooting & Cleaning

If you encounter issues such as stuck networks, orphaned containers, or want to fully rebuild your environment, you can use the following commands.

### 1. Stop and remove all containers, networks, volumes, and images for this compose project:

```bash
docker-compose -f docker-compose-wgp-images.yml --env-file .env down --rmi all --volumes --remove-orphans
```

- `--rmi all` → removes all images built or used by this compose file  
- `--volumes` → removes named and anonymous volumes  
- `--remove-orphans` → removes containers not defined in the compose file  

This is useful if you want to **start fresh** or free disk space.

---

### 2. Check which containers or networks are still running

```bash
docker ps -a
docker network ls
```

- Stop/remove any leftover containers manually if needed:  
```bash
docker rm -f <container_id>
docker network rm <network_name>
```

---

### 3. Common issues

- **Network is still in use** → usually caused by orphaned containers attached to the network.  
- **Volumes not removed** → some containers may have mounted volumes still in use. Use `--volumes` with `down` or remove manually.  
- **Images not rebuilt** → make sure to use `--build` with `up` if you changed Dockerfiles or the compose file.