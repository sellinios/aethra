#!/bin/bash

# Change to the project directory
cd /home/sellinios/aethra

# Run the Django management command inside the Docker container using the container's Python environment
docker-compose exec backend /usr/local/bin/python manage.py gfs_data_download

# No need to deactivate the virtual environment, as it's not used inside the container
