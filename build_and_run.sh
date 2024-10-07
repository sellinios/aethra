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

# Step 2: Build the frontend
echo "Building frontend..."
cd frontend || { echo "Frontend directory not found"; exit 1; }

# Install dependencies if necessary
if [ ! -d "node_modules" ]; then
  echo "Installing frontend dependencies..."
  npm install
fi

# Build the frontend project
npm run build
if [ $? -ne 0 ]; then
  echo "Frontend build failed!"
  exit 1
fi
echo "Frontend build completed."

# Step 3: Copy build files to the backend static directory
echo "Copying build files to the static directory..."
cp -r build/* ../backend/static/  # Adjust the path as needed for your static files

# Step 4: Go back to the root directory
cd ..

# Step 5: Start Docker containers
echo "Starting Docker containers..."
docker-compose up --build -d
if [ $? -ne 0 ]; then
  echo "Failed to start Docker containers!"
  exit 1
fi

# Step 6: Check the status of containers
docker-compose ps

echo "All services should be up and running."
