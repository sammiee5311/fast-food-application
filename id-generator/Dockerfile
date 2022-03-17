FROM python

WORKDIR /app

EXPOSE 8008

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./