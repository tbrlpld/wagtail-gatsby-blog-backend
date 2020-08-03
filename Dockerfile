# Use an official Python runtime as a parent image
FROM python:3.7
LABEL maintainer="hello@wagtail.io"

# Set the working directory to /code/
WORKDIR /code/

# Prepare dependency installation
RUN pip install --upgrade pip
RUN pip install poetry

# Create non-default user 
# Since I am using the venv, I will not need to be root after this point
RUN useradd wagtail
RUN mkdir /home/wagtail
RUN chown -R wagtail /home/wagtail
RUN chown -R wagtail /code
USER wagtail

# Pull repo
RUN git clone https://github.com/tbrlpld/wagtail-gatsby-blog-backend.git .

# Install any needed packages
RUN poetry env use system
RUN poetry install 

# Add .env file
COPY ./.env /code/.env

# RUN $(poetry env info --path)/bin/python manage.py migrate
# RUN $(poetry env info --path)/bin/python manage.py collectstatic --noinput

EXPOSE 8000
# CMD exec $(poetry env info --path)/bin/gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 3 --error-logfile - --log-file - --log-level debug
CMD /code/bin/runserver.sh