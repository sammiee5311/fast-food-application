UNAME := $(shell uname)

ifeq ($(OSTYPE), Windows_NT)
	PYTHON := python
	PIP := pip
else
	PYTHON := python3
	PIP := pip3
endif

make-env:
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
	$(PIP) install -r requirements.txt

run-docker-compose:
	docker-compose -f kafka/docker-compose.yml up -d

stop-docker-compose:
	docker-compose -f kafka/docker-compose.yml down

set-up-django:
	( \
		cd django; \
		$(PIP) install -r requirements.txt; \
		python manage.py makemigrations; \
		python manage.py migrate; \
	)

test-run-samples:
	$(PYTHON) tests/test_run_samples.py

test-django:
	cd django &&\
		coverage run manage.py test

dependency: install

unittest: set-up-django test-django

kafka-docker: run-docker-compose test-run-samples stop-docker-compose

all: dependency unittest kafka-docker
