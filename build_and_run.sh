#!/bin/bash

# Step 0: Ensure necessary tools are installed
# Ensure pip-review is installed
if ! command -v pip-review &> /dev/null
then
    echo "pip-review could not be found, installing it..."
    pip install pip-review
fi

# Ensure npm is installed
if ! command -v npm &> /dev/null
then
    echo "npm could not be found, please install it."
    exit 1
fi

# Step 0.5: Kill non-production servers (Django and React)
echo "Killing non-production Django and React servers..."
pkill -f runserver && pkill -f node
if [ $? -ne 0 ]; then
  echo "No development servers found or failed to kill some processes!"
fi

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

# Frontend projects to build
frontends=("frontend_kairos" "frontend_fthina")

# Corresponding static directory names
static_dirs=("kairos" "fthina")

# Step 2: Build frontend projects
cd frontend || { echo "frontend directory not found"; exit 1; }

for i in "${!frontends[@]}"; do
    frontend="${frontends[$i]}"
    static_dir="${static_dirs[$i]}"
    echo "Building ${frontend}..."
    cd $frontend || { echo "${frontend} directory not found"; exit 1; }

    # Install dependencies if necessary
    if [ ! -d "node_modules" ]; then
      echo "Installing ${frontend} dependencies..."
      npm install
    fi

    # Build the frontend project
    npm run build
    if [ $? -ne 0 ]; then
      echo "${frontend} build failed!"
      exit 1
    fi
    echo "${frontend} build completed."

    # Ensure the static directory exists
    mkdir -p ../../backend/static/${static_dir}/

    # Copy build files to the backend static directory
    echo "Copying ${frontend} build files to the ${static_dir} static directory..."
    cp -r build/* ../../backend/static/${static_dir}/

    # Go back to the frontend directory
    cd ..
done

# Step 3: Go back to the root directory
cd ..

# Step 4: Start Docker containers
echo "Starting Docker containers..."
docker-compose up --build -d
if [ $? -ne 0 ]; then
  echo "Failed to start Docker containers!"
  exit 1
fi

# Step 5: Check the status of containers
docker-compose ps
docker volume ls
docker network ls

echo "All services should be up and running."
