#!/bin/bash 

set -0 errexit 

set -0 fipefail 

set -0 nounset 

python manage.py migrate --no-input 
python manage.py collectstatic --no-input 
exec python manage.py runserver 0.0.0.0:8000