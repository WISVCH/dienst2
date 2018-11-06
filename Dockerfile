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
    apt-get update && \
    apt-get install -y --no-install-recommends libldap2-dev libsasl2-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    cp dienst2/local.py.ci dienst2/local.py && \
    ./manage.py collectstatic --noinput && \
    apt-get purge -y libldap2-dev libsasl2-dev && \
    apt-get autoremove -y && \
    rm -rf dienst2/local.py* /var/lib/apt/lists/* /usr/lib/node_modules node_modules

RUN groupadd -r dienst2 --gid=999 && useradd --no-log-init -r -g dienst2 --uid=999 dienst2
USER 999

ENTRYPOINT ["/srv/docker-entrypoint.sh"]
CMD ["gunicorn"]
EXPOSE 8000
