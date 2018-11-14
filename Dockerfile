FROM node AS node

WORKDIR /src
COPY . .
RUN yarn install --flat

FROM python:3.7

# CH CA certificate for PostgreSQL TLS connections
ADD https://ch.tudelft.nl/certs/wisvch.crt /usr/local/share/ca-certificates/wisvch.crt
RUN chmod 0644 /usr/local/share/ca-certificates/wisvch.crt && \
    update-ca-certificates

RUN mkdir -p /srv
WORKDIR /srv
COPY . /srv
COPY --from=node /src/dienst2/static/lib /srv/dienst2/static/lib

RUN pip install --no-cache-dir -r requirements.txt
RUN set -a && . ./ci.env && ./manage.py collectstatic --noinput

RUN groupadd -r dienst2 --gid=999 && useradd --no-log-init -r -g dienst2 --uid=999 dienst2
USER 999

ENTRYPOINT ["/srv/docker-entrypoint.sh"]
CMD ["gunicorn"]
EXPOSE 8000
