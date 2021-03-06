# Use an official Python runtime as a parent image
FROM python:3.7
LABEL maintainer="tibor@lpld.io"

# Install cron and configure cron
# https://stackoverflow.com/questions/37458287/how-to-run-a-cron-job-inside-a-docker-container
COPY ./docker/wagtail/wagtailcron /etc/cron.d/wagtailcron 
RUN apt-get update -qq \
	&& apt-get -y install -qq cron \
	&& chmod 0644 /etc/cron.d/wagtailcron \
	&& crontab /etc/cron.d/wagtailcron

# Set the working directory to /code/
WORKDIR /code/

# Prepare dependency installation
RUN pip install --upgrade pip && pip install poetry

# Copy dependency definition from local to image.
# It will trigger a rebuild of the image in case the dependencies have changed.
COPY ./pyproject.toml /code/pyproject.toml
COPY ./poetry.lock /code/poetry.lock
# Install dependencies
RUN poetry env use system && poetry install 

# Add all local code to the image.
COPY . /code/

EXPOSE 8000
CMD /code/container/runapp.sh