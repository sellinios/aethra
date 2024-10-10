#!/bin/bash

# Step 1: Update Python dependencies in the backend
echo "Updating Python dependencies..."
pip-review --local --auto
if [ $? -ne 0 ]; then
  echo "Failed to update Python dependencies!"
  exit 1
fi

# Freeze the dependencies into requirements.txt
pip freeze > backend/requirements.txt
echo "Python dependencies updated."

# Step 2: Build the Kairos frontend
echo "Building frontend_kairos..."
cd frontend/frontend_kairos || { echo "frontend_kairos directory not found"; exit 1; }

# Install dependencies if necessary
if [ ! -d "node_modules" ]; then
  echo "Installing frontend_kairos dependencies..."
  npm install
fi

# Build the frontend project
npm run build
if [ $? -ne 0 ]; then
  echo "frontend_kairos build failed!"
  exit 1
fi
echo "frontend_kairos build completed."

# Step 3: Copy build files to the backend static directory for kairos
echo "Copying frontend_kairos build files to the kairos static directory..."
cp -r build/* ../../backend/static/kairos/

# Step 4: Build the Fthina frontend
echo "Building frontend_fthina..."
cd ../frontend_fthina || { echo "frontend_fthina directory not found"; exit 1; }

# Install dependencies if necessary
if [ ! -d "node_modules" ]; then
  echo "Installing frontend_fthina dependencies..."
  npm install
fi

# Build the frontend project
npm run build
if [ $? -ne 0 ]; then
  echo "frontend_fthina build failed!"
  exit 1
fi
echo "frontend_fthina build completed."

# Step 5: Copy build files to the backend static directory for fthina
echo "Copying frontend_fthina build files to the fthina static directory..."
cp -r build/* ../../backend/static/fthina/

# Step 6: Go back to the root directory
cd ../../

# Step 7: Start Docker containers
echo "Starting Docker containers..."
docker-compose up --build -d
if [ $? -ne 0 ]; then
  echo "Failed to start Docker containers!"
  exit 1
fi

# Step 8: Check the status of containers
docker-compose ps

echo "All services should be up and running."
