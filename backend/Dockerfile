# Use the official Python image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    dos2unix \
    netcat-openbsd  # Changed from 'netcat' to 'netcat-openbsd'

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
