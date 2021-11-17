env:
	python3 -m venv venv &&\
		source ./venv/bin/activate

run-docker-compose:
	docker-compose -f ./kafka/docker-compose.yml up -d

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test-run-samples:
	python tests/test_run_samples.py

stop-docker-compose:
	docker-compose -f ./kafka/docker-compose.yml down

all: env install run-docker-compose test-run-samples stop-docker-compose
