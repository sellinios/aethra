# Use the official Python image
FROM python:3.12-slim

# Install system dependencies including GDAL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    curl \
    dos2unix \
    netcat-openbsd  # Changed from 'netcat' to 'netcat-openbsd'

# Set environment variable for GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal \
    C_INCLUDE_PATH=/usr/include/gdal

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Install python-dotenv
RUN pip install python-dotenv

# Copy project files
COPY . /code/

# Convert entrypoint.sh to Unix format and ensure it's executable
RUN dos2unix /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# Expose port
EXPOSE 8000

# Start the application
CMD ["/bin/sh", "./entrypoint.sh"]
