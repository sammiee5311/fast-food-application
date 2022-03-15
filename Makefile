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

run-database:
	docker-compose -f django/docker-compose.yml up -d

stop-database:
	docker-compose -f django/docker-compose.yml down

set-up-backend:
	( \
		cd django; \
		$(PIP) install -r requirements.txt; \
		$(PYTHON) manage.py makemigrations; \
		$(PYTHON) manage.py migrate; \
	)

set-up-deployment:
	cd machine-learning-api &&\
		$(PIP) install -r requirements.txt

test-deployment:
	cd machine-learning-api &&\
		$(PYTHON) -m pytest

set-up-tracking:
	cd tracking &&\
		npm install

test-tracking:
	cd tracking &&\
		npm test

test-run-samples:
	( \
		$(PIP) install -r tests/requirements.txt; \
		$(PYTHON) tests/test_run_samples.py; \
	)

set-up-order-delivery-time-handler:
	cd order-delivery-time-handler &&\
		$(PIP) install -r requirements.txt

test-order-delivery-time-handler:
	cd order-delivery-time-handler &&\
		$(PYTHON) -m pytest	

test-backend:
	cd django &&\
		coverage run manage.py test

backend-server: set-up-backend test-backend

deployment: set-up-deployment test-deployment

tracking: set-up-tracking test-tracking

order-delivery-time-handler: set-up-order-delivery-time-handler test-order-delivery-time-handler

kafka-docker: run-docker-compose test-run-samples stop-docker-compose