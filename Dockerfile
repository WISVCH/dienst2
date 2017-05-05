FROM python:3.6

# CH CA certificate for LDAP and PostgreSQL TLS connections
RUN curl -so /usr/local/share/ca-certificates/wisvch.crt https://ch.tudelft.nl/certs/wisvch.crt && \
    chmod 644 /usr/local/share/ca-certificates/wisvch.crt && \
    update-ca-certificates

# Build dependencies for pyldap + runtime dependencies for django_compressor (coffee, lessc)
RUN export DEBIAN_FRONTEND="noninteractive" && \
    apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install -y --no-install-recommends libldap2-dev libsasl2-dev coffeescript node-less && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /srv
WORKDIR /srv

COPY . /srv
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir newrelic gunicorn

ENTRYPOINT ["/srv/docker-entrypoint.sh"]
EXPOSE 8000
CMD ["gunicorn"]
