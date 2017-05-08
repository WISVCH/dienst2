FROM python:3.6

# CH CA certificate for LDAP and PostgreSQL TLS connections
RUN curl -so /usr/local/share/ca-certificates/wisvch.crt https://ch.tudelft.nl/certs/wisvch.crt && \
    chmod 644 /usr/local/share/ca-certificates/wisvch.crt && \
    update-ca-certificates

RUN mkdir -p /srv
WORKDIR /srv
COPY . /srv

RUN export DEBIAN_FRONTEND="noninteractive" && \
    apt-get update && \
    apt-get dist-upgrade -y && \
    curl -sL https://deb.nodesource.com/setup_6.x | bash - && \
    apt-get install -y --no-install-recommends libldap2-dev libsasl2-dev nodejs && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt newrelic gunicorn && \
    npm install -g bower less coffee-script && \
    bower --allow-root install && \
    cp dienst2/local.py.example dienst2/local.py && \
    ./manage.py collectstatic --noinput && \
    ./manage.py compress && \
    apt-get purge -y libldap2-dev libsasl2-dev nodejs && \
    apt-get autoremove -y && \
    rm -rf dienst2/local.py /var/lib/apt/lists/* /usr/lib/node_modules

ENTRYPOINT ["/srv/docker-entrypoint.sh"]
EXPOSE 8000
CMD ["gunicorn"]
