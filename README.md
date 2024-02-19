## Features
* cli import
* django rest framework data import endpoint
* thread pool to handle big files
* pipenv
* dotenv
* docker compose file
* logger
* unittests

## Setup
Built using python 3.11
```commandline
python -m pip install pipenv
pipenv install

# setup DB
docker compose up

cp .env.example .env
python manage.py migrate
python manage.py createsuperuser

# run server 
python manage.py 0.0.0.0:8000  --noreload

# to import using cli
python manage.py data_import --file examples/pois.csv --file examples/pois.xml

# to run unittests
python manage.py test point_of_interest/tests

```

