# Use an official Python runtime as a parent image
FROM python:3.7
LABEL maintainer="hello@wagtail.io"

# Set environment varibles
ENV DJANGO_SETTINGS_MODULE="mysite.settings.production"

# Set the working directory to /code/
WORKDIR /code/

# Prepare dependency installation
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry env use system
RUN poetry config virtualenvs.create false

# Pull repo
RUN git clone https://github.com/tbrlpld/wagtail-gatsby-blog-backend.git .

# Install any needed packages
RUN poetry install 
RUN poetry add gunicorn

RUN python manage.py migrate

# Create non-default user
RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail

EXPOSE 8000
CMD exec gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 3