UNAME := $(shell uname)

ifeq ($(OSTYPE), Windows_NT)
	PYTHON := python
	PIP := pip
else
	PYTHON := python3
	PIP := pip3
endif

create-env:
	$(PYTHON) -m venv venv

install-env:
ifeq ($(OSTYPE), Windows_NT)
	( \
		./venv/bin/activate; \
		$(PIP) install -r requirements.txt; \
	)
else ifeq ($(UNAME), Linux)
	( \
		. venv/bin/activate; \
		$(PIP) install -r requirements.txt; \
	)
else
	( \
		source venv/bin/activate; \
		$(PIP) install -r requirements.txt; \
	)
endif

install:
	$(PIP) install -r samples/requirements.txt

run-docker-compose:
	docker-compose -f kafka/docker-compose.yml up -d --build

stop-docker-compose:
	docker-compose -f kafka/docker-compose.yml down

set-up-django:
	( \
		cd django; \
		$(PIP) install -r requirements.txt; \
		$(PYTHON) manage.py makemigrations; \
		$(PYTHON) manage.py migrate; \
	)

set-up-flask:
	cd data-handling &&\
		$(PIP) install -r requirements.txt; \

test-flask:
	cd data-handling &&\
		$(PYTHON) -m pytest

test-run-samples:
	( \
		$(PIP) install -r tests/requirements.txt; \
		$(PYTHON) tests/test_run_samples.py; \
	)
	

test-django:
	cd django &&\
		coverage run manage.py test

dependency: install

unittest: set-up-django test-django

pytest: set-up-flask test-flask

kafka-docker: run-docker-compose test-run-samples stop-docker-compose

all: dependency unittest kafka-docker
