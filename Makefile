env:
ifeq ($(OSTYPE), Windows_NT)
	python -m venv venv &&\
		./venv/Scripts/activate
else
	python3 -m venv venv &&\
		source ./venv/bin/activate
endif

install:
ifeq ($(OSTYPE), Windows_NT)
	pip install -r requirements.txt
else
	pip install --upgrade pip &&\
		pip install -r requirements.txt
endif

run-docker-compose:
	docker-compose -f ./kafka/docker-compose.yml up -d

stop-docker-compose:
	docker-compose -f ./kafka/docker-compose.yml down

set-up-django:
	cd django &&\
		pip install -r requirements.txt &&\
			python manage.py makemigrations &&\
				python manage.py migrate

test-run-samples:
	python tests/test_run_samples.py

test-django:
	cd django &&\
		coverage run manage.py test

all: env install run-docker-compose test-run-samples stop-docker-compose

unittest: set-up-django test-django