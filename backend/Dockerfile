# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /backend

COPY /app/requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000
ENV app=app/
#ENTRYPOINT [ "flask", "--app", "app/", "init-db" ]
RUN flask init-db
ENTRYPOINT [ "flask"]
#CMD ["flask","--app", "app/", "init-db"]
#CMD [ "flask","--app", "app/", "run", "--host=0.0.0.0"]