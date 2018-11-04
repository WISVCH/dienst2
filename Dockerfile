FROM python:3.7-stretch

# CH CA certificate for LDAP and PostgreSQL TLS connections
RUN curl -so /usr/local/share/ca-certificates/wisvch.crt https://ch.tudelft.nl/certs/wisvch.crt && \
    chmod 644 /usr/local/share/ca-certificates/wisvch.crt && \
    update-ca-certificates

RUN mkdir -p /srv
WORKDIR /srv
COPY . /srv

RUN export DEBIAN_FRONTEND="noninteractive" && \
    curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends libldap2-dev libsasl2-dev nodejs yarn && \
    yarn install && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    cp dienst2/local.py.ci dienst2/local.py && \
    ./manage.py collectstatic --noinput && \
    ./manage.py compress && \
    apt-get purge -y libldap2-dev libsasl2-dev nodejs yarn && \
    apt-get autoremove -y && \
    rm -rf dienst2/local.py* /var/lib/apt/lists/* /usr/lib/node_modules node_modules

RUN groupadd -r dienst2 --gid=999 && useradd --no-log-init -r -g dienst2 --uid=999 dienst2
USER 999

ENTRYPOINT ["/srv/docker-entrypoint.sh"]
CMD ["gunicorn"]
EXPOSE 8000
