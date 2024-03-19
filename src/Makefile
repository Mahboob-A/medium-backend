

# ### Docker management commands 
 
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

docker-restart-api: 
	docker compose -f dev.yml restart api 

docker-exec-api: 
	docker compose -f dev.yml exec api /bin/bash 

# ## 


# ### Docker Volume and Postgres Database 

docker-volume: 
	docker volume inspect src_dev_postgres_data

docker-exec-postgres: 
	docker compose -f dev.yml exec postgres /bin/bash 

medium-database: 
	docker compose -f dev.yml exec postgres psql --username=mahboob --dbname=medium-db 

# ## 




# ### Services logs commands 

docker-logs-celery:
	docker compose -f dev.yml logs celery_worker

docker-logs-redis:
	docker compose -f dev.yml logs redis

docker-logs-flower:
	docker compose -f dev.yml logs flower

docker-logs-mailhog:
	docker compose -f dev.yml logs mailhog

docker-logs-postgres: 
	docker compose -f dev.yml logs postgres

# ## 




# ### Elastic Search Commands 
# create-es-index command (--create) only creates the index. after creating the index, we need to populate it.  
create-es-index: 
	docker compose -f dev.yml exec api python manage.py search_index --create 

# populate-es-index command (--populate) populates the index. 
populate-es-index: 
	docker compose -f dev.yml exec api python manage.py search_index --populate

# this commad do the both - create and populate (--rebuild)
es-create-populate-index: 
	docker compose -f dev.yml exec api python manage.py search_index --rebuild 

# ##




# ### Django Commands

makemigrations: 
	docker compose -f dev.yml run --rm api python manage.py makemigrations

migrate: 
	docker compose -f dev.yml run --rm api python manage.py migrate

collectstatic: 
	docker compose -f dev.yml run --rm api python manage.py collectstatic --no-input --clear 

superuser: 
	docker compose -f dev.yml run --rm api python manage.py createsuperuser 

# ## 




# ### Pytest Commands
pytest-no-wrn-codecov:
	docker compose -f dev.yml run --rm api pytest -p no:warnigns --cov=. -v  

pytest-no-wrn-codecov-html:
	docker compose -f dev.yml run --rm api pytest -p no:warnigns --cov=. --cov-report html



# ### Other Tools for Formatting 

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

# ## 