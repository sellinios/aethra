#!/bin/bash

# Step 1: Build the frontend
echo "Building frontend..."
cd frontend || { echo "Frontend directory not found"; exit 1; }

# Install dependencies if necessary
if [ ! -d "node_modules" ]; then
  echo "Installing frontend dependencies..."
  npm install
fi

# Build the frontend project (adjust command if you're using a different build tool)
npm run build

# Check if the build was successful
if [ $? -ne 0 ]; then
  echo "Frontend build failed!"
  exit 1
fi

echo "Frontend build completed."

# Step 2: Move the build files to the appropriate directory (if needed)
# Assuming your Docker configuration expects the build files in a specific location
# Adjust this based on your project structure. If Docker serves the build directly from the `frontend/build/` folder, you can skip this.
echo "Copying build files to the static directory..."
cp -r build/* ../backend/static/  # Adjust path to where your backend serves static files

# Step 3: Go back to the root directory
cd ..

# Step 4: Run docker-compose to start all services
echo "Starting Docker containers..."
docker-compose up --build -d

# Step 5: Check the status of containers
docker-compose ps

echo "All services should be up and running."
