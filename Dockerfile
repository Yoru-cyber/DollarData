# Use a Python base image with Poetry pre-installed
FROM python:3.11.11-slim-bookworm

# Set the working directory inside the container
WORKDIR /app

# Copy the Poetry configuration files
COPY . /app

# Install system dependencies if needed (e.g., for certain libraries)
# Example:
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# Install project dependencies using Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --without dev


CMD [ "gunicorn" ]