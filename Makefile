clean:
	find . -name "*.pyc" | xargs rm | true
	find . -name __pycache__ -type d -empty -delete

py_env:
	pip install -r requirements.txt

build_image:
	docker build -t rip_docker .

start_db: build_image
	docker-compose up db

turn_up: start_db
	docker-compose up

turn_down:
	docker-compose down

access_running_web:
	docker-compose exec web /bin/bash

all: clean py_env
