FROM node AS node

WORKDIR /src
COPY . .
RUN yarn install --flat

FROM python:3.7-stretch

# CH CA certificate for LDAP and PostgreSQL TLS connections
RUN curl -so /usr/local/share/ca-certificates/wisvch.crt https://ch.tudelft.nl/certs/wisvch.crt && \
    chmod 644 /usr/local/share/ca-certificates/wisvch.crt && \
    update-ca-certificates

RUN mkdir -p /srv
WORKDIR /srv
COPY . /srv
COPY --from=node /src/dienst2/static/lib /srv/dienst2/static/lib

RUN export DEBIAN_FRONTEND="noninteractive" && \
    pip install --no-cache-dir -r requirements.txt && \
    cp dienst2/local.py.ci dienst2/local.py && \
    ./manage.py collectstatic --noinput && \
    rm -rf dienst2/local.py*

RUN groupadd -r dienst2 --gid=999 && useradd --no-log-init -r -g dienst2 --uid=999 dienst2
USER 999

ENTRYPOINT ["/srv/docker-entrypoint.sh"]
CMD ["gunicorn"]
EXPOSE 8000
