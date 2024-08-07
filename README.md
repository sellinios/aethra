pip-review --local --auto
pip freeze > requirements.txt
docker info | grep Swarm
docker service ls
docker ps 
docker exec -it (ID here) bash
docker stack deploy -c docker-stack.yml aethra
./deploy-swarm.sh

docker service logs aethra_backend
docker service logs aethra_db
docker service logs aethra_frontend
docker service logs aethra_nginx-frontend
docker service logs aethra_nginx-backend

docker service inspect aethra_backend
docker service inspect aethra_backend
docker service inspect aethra_db
docker service inspect aethra_frontend
docker service inspect aethra_nginx-frontend
docker service inspect aethra_nginx-backend

tree -L 5 -I 'node_modules|build|venv|staticfiles'

docker stack rm aethra
docker system prune -a

docker exec -it $(docker ps --filter name=aethra_backend -q | head -n1) python manage.py collectstatic --noinput
docker exec -it $(docker ps --filter name=aethra_backend -q | head -n1) python manage.py migrate
