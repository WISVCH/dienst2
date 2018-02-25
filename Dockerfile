FROM python:3.6-stretch

# CH CA certificate for LDAP and PostgreSQL TLS connections
RUN curl -so /usr/local/share/ca-certificates/wisvch.crt https://ch.tudelft.nl/certs/wisvch.crt && \
    chmod 644 /usr/local/share/ca-certificates/wisvch.crt && \
    update-ca-certificates

RUN mkdir -p /srv
WORKDIR /srv
COPY . /srv

RUN export DEBIAN_FRONTEND="noninteractive" && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    apt-get install -y --no-install-recommends libldap2-dev libsasl2-dev nodejs && \
    npm install -g bower less coffee-script && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt ddtrace gunicorn && \
    bower --allow-root install && \
    ./manage.py collectstatic --noinput && \
    ./manage.py compress && \
    apt-get purge -y libldap2-dev libsasl2-dev nodejs && \
    apt-get autoremove -y && \
    rm -rf dienst2/local.py* /var/lib/apt/lists/* /usr/lib/node_modules

RUN groupadd -r dienst2 --gid=999 && useradd --no-log-init -r -g dienst2 --uid=999 dienst2
USER dienst2

ENTRYPOINT ["/srv/docker-entrypoint.sh"]
CMD ["gunicorn"]
EXPOSE 8000
