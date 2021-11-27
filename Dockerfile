FROM python:alpine3.10
COPY . /kreeper
WORKDIR /kreeper
CMD python3 kreeper.py