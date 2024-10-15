#!/bin/bash

# Activate the virtual environment
source /home/sellinios/aethra/venv/bin/activate

# Change to the project directory
cd /home/sellinios/aethra

# Run the Django management command inside the Docker container
docker-compose exec backend python manage.py run_gfs_pipeline

# Deactivate the virtual environment (optional)
deactivate
