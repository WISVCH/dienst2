FROM mcr.microsoft.com/devcontainers/python:3-3.11@sha256:cbd8462c5f978ee054c1ef2f3493033c2efbe56c7b51a7ed32439d76b19b3636

COPY pyproject.toml /
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

ENV PYTHONUNBUFFERED 1

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --with dev
