install_and_run:
	sudo docker compose -f infra/docker-compose.production.yml pull
	sudo docker compose -f infra/docker-compose.production.yml down
	sudo docker compose -f infra/docker-compose.production.yml up -d
	sudo docker compose -f infra/docker-compose.production.yml exec backend python manage.py migrate
	sudo docker compose -f infra/docker-compose.production.yml exec backend python manage.py collectstatic
	sudo docker compose -f infra/docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/

create_superuser:
	sudo docker compose -f infra/docker-compose.production.yml exec backend python manage.py createsuperuser

load_ingredients:
	sudo docker compose -f infra/docker-compose.production.yml exec backend python manage.py load_csv
