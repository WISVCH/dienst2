FROM mcr.microsoft.com/devcontainers/python:0-3.11

COPY pyproject.toml /
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

ENV PYTHONUNBUFFERED 1

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --with dev
