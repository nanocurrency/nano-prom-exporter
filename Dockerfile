FROM python:3.8-alpine

WORKDIR /app
COPY . /app

RUN apk --update-cache add --virtual build-dependencies build-base linux-headers \
    && pip install -r requirements.txt \
    && python setup.py install \
    && apk del build-dependencies 

ENTRYPOINT [ "nano-prom" ]