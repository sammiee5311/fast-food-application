FROM python:3.10.0

RUN apt-get install gcc

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./