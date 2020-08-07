# Use an official Python runtime as a parent image
FROM python:3.7
LABEL maintainer="tibor@lpld.io"

# Set the working directory to /code/
WORKDIR /code/

# Prepare dependency installation
RUN pip install --upgrade pip
RUN pip install poetry

# Create non-default user 
# Since poetry will be using a venv there is no more need for root access
RUN useradd wagtail
RUN mkdir /home/wagtail
RUN chown -R wagtail /home/wagtail
RUN chown -R wagtail /code
USER wagtail

# Copy dependency definition from local to image.
# It will trigger a rebuild of the image in case the dependencies have changed.
COPY --chown=wagtail ./pyproject.toml /code/pyproject.toml
COPY --chown=wagtail ./poetry.lock /code/poetry.lock
# Install dependencies
RUN poetry env use system
RUN poetry install 

# Add all local code to the image.
COPY --chown=wagtail . /code/

EXPOSE 8000
CMD /code/container/runapp.sh