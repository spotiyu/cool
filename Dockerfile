FROM python:3.8-slim

ADD . /real-url-api
WORKDIR /real-url-api

RUN apt-get update -y &&\
    pip install --upgrade pip &&\
    pip install pipreqs &&\
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["pipreqs . --prints"]
