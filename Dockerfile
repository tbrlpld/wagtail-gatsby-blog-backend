# Use an official Python runtime as a parent image
FROM python:3.7
LABEL maintainer="tibor@lpld.io"

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

# Initialize git repo. This is be able to pull changes later on.
RUN git config --global user.name "Tibor Leupold"
RUN git config --global user.email "tibor@lpld.io"
RUN git clone https://github.com/tbrlpld/wagtail-gatsby-blog-backend.git .

# Copy dependency definition from local to image. This is mainly for development.
# It will trigger a rebuild of the image in case the dependencies have changed.
COPY --chown=wagtail ./pyproject.toml /code/pyproject.toml
COPY --chown=wagtail ./poetry.lock /code/poetry.lock
# Install dependencies
RUN poetry env use system
RUN poetry install 

# Add all local code to the image. This mainly makes testing of the production setup
# easier as a rebuild can contain data that is not pushed to GitHub. 
# The code directory will be overridden with a mounted volume anyways during runtime.
COPY --chown=wagtail . /code/

EXPOSE 8000
CMD /code/container/runapp.sh