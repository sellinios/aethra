# Django and React Project Setup

## Project Structure

To view the project structure, run:

```bash
tree -L 5 -I 'node_modules|build|venv|static'
```

## Dependency Management

Update and freeze Python dependencies:

```bash
pip-review --local --auto
pip freeze > requirements.txt
```

Generate a secure token:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

## Environment Variables

Set the Django environment variables:

```bash
export DJANGO_ENVIRONMENT=development
export DJANGO_ENV_FILE=.env.development
```

## Frontend Build

Build the frontend application:

```bash
npm run build
sudo docker-compose build --no-cache frontend
```

## Docker Management

List Docker volumes and networks:

```bash
docker volume ls
docker network ls
```

### Start/Stop Docker Containers

Bring down the containers:

```bash
docker-compose down
```

Bring up the containers with rebuild:

```bash
docker-compose -f compose.yaml up -d --build
docker-compose -f compose.yaml up -d --build backend
docker-compose -f compose.yaml up -d --build frontend
```

### Running Containers

Start all containers:

```bash
sudo docker-compose up -d
```

View the status of the containers:

```bash
sudo docker-compose ps
```

## Database Management

Run migrations and collect static files:

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py run_gfs_pipeline
docker-compose exec backend python manage.py collectstatic --noinput
```

## Cleanup

Remove stopped containers:

```bash
docker container prune
```

Remove unused images:

```bash
docker image prune
```

Remove unused volumes:

```bash
docker volume prune
```

Remove all unused Docker data:

```bash
docker system prune
```
