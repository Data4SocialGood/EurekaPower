# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /frontend

COPY /requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
ENV FLASK_APP=./front.py
#ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=5001"]
ENTRYPOINT [ "flask" ]