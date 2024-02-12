docker-up: 
	docker compose -f dev.yml up --build -d --remove-orphans 

docker-down: 
	docker compose -f dev.yml down

docker-down-v: 
	docker compose -f dev.yml down -v

docker-logs: 
	docker compose -f dev.yml logs 

docker-logs-api: 
	docker compose -f dev.yml logs api 

makemigrations: 
	docker compose -f dev.yml run --rm api python manage.py makemigrations

migrate: 
	docker compose -f dev.yml run --rm api python manage.py migrate

collectstatic: 
	docker compose -f dev.yml run --rm api python manage.py collectstatic --no-input --clear 

superuser: 
	docker compose -f dev.yml run --rm api python manage.py createsuperuser 

docker-volume: 
	docker volume inspect src_dev_postgres_data

medium-database: 
	docker compose -f dev.yml exec postgres psql --username=mahboob --dbname=medium-db 

flake8: 
	docker compose -f dev.yml exec api flake8 . 

black-check: 
	docker compose -f dev.yml exec api black --check --exclude=migrations . 

black-diff: 
	docker compose -f dev.yml exec api black --diff --exclude=migrations . 

black: 
	docker compose -f dev.yml exec api black --exclude=migrations . 

isort-check: 
	docker compose -f dev.yml exec api isort . --check-only --skip venv --skip migrations 

isort-diff: 
	docker compose -f dev.yml exec api isort . --diff --skip venv --skip migrations

isort: 
	docker compose -f dev.yml exec api isort . --skip venv --skip migrations
