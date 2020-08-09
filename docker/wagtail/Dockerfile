# Use an official Python runtime as a parent image
FROM python:3.7
LABEL maintainer="tibor@lpld.io"

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