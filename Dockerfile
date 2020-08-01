# Use an official Python runtime as a parent image
FROM python:3.7
LABEL maintainer="hello@wagtail.io"

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev

# Set the working directory to /code/
WORKDIR /code/

# Prepare dependency installation
# COPY ./requirements.txt /code/requirements.txt
COPY ./pyproject.toml /code/pyproject.toml
COPY ./poetry.lock /code/poetry.lock
RUN pip install --upgrade pip
RUN pip install poetry

# Install any needed packages specified in requirements.txt
# RUN pip install -r /code/requirements.txt
# RUN poetry shell
RUN poetry env use system
RUN poetry config virtualenvs.create false
RUN poetry install 
RUN poetry add gunicorn

# Copy the current directory contents into the container at /code/
COPY . /code/

RUN python manage.py migrate

# Create non-default user
RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail

EXPOSE 8000
# CMD exec gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 3
CMD exec python manage.py runserver 0:8000