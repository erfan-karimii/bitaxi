FROM docker.arvancloud.ir/python:3.11.1-slim


ENV PYTHONUNBUFFERED 1


ADD requirements/ requirements/
RUN pip install -r requirements/dev.txt

# Get the django project into the docker container
RUN mkdir /app
WORKDIR /app
ADD ./core/ /app/