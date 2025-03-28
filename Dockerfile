FROM node AS node

WORKDIR /src
COPY . .
RUN yarn install --flat

FROM python:3.11

RUN mkdir -p /srv
WORKDIR /srv
COPY . /srv
COPY --from=node /src/dienst2/static/lib /srv/dienst2/static/lib
RUN export DEBIAN_FRONTEND="noninteractive" && \
    apt-get update && \
    pip install poetry && \
    apt-get autoremove -y && \
    rm -rf /tmp/* /var/lib/apt/lists/*

RUN poetry config virtualenvs.create false
RUN poetry install --no-root
RUN set -a && . ./ci.env && python manage.py collectstatic --noinput --no-post-process

RUN groupadd -r dienst2 --gid=999 && useradd --no-log-init -r -g dienst2 --uid=999 dienst2
USER 999

ENTRYPOINT ["/srv/docker-entrypoint.sh"]
CMD ["gunicorn"]
EXPOSE 8000
