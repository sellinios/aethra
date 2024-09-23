tree -L 5 -I 'node_modules|build|venv|staticfiles'
sudo docker-compose build --no-cache
sudo docker-compose up -d
sudo docker-compose ps
docker-compose exec backend python manage.py migrate
