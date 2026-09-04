# syntax=docker/dockerfile:1

FROM node:24-bookworm AS frontend

WORKDIR /src
# Node 24 still provides Corepack's Yarn shims; Node 25+ does not. Remove the
# shims so the same explicitly pinned Yarn installation works on both.
RUN rm -f /usr/local/bin/yarn /usr/local/bin/yarnpkg \
 && npm install --global yarn@1.22.22

# Install frontend dependencies before application code so this layer is reused
# unless the dependency manifest changes.
COPY package.json yarn.lock .yarnrc ./
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn \
    yarn install --frozen-lockfile --flat


FROM python:3.14 AS dependencies

WORKDIR /srv

ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install "poetry==2.4.2"

# Install production dependencies before application code so this layer is
# reused unless pyproject.toml or poetry.lock changes.
COPY pyproject.toml poetry.lock ./
RUN --mount=type=cache,target=/root/.cache/pypoetry \
    poetry install --only main --no-root


FROM python:3.14 AS runtime

WORKDIR /srv

ENV PATH="/srv/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd --system --gid 999 dienst2 \
 && useradd --system --uid 999 --gid dienst2 --no-log-init dienst2

COPY --from=dependencies /srv/.venv /srv/.venv
# dev.env is local runtime configuration and must not be included in the
# production image.
COPY --exclude=dev.env . /srv
COPY --from=frontend /src/dienst2/static/lib /srv/dienst2/static/lib

# ci.env supplies harmless build-time Django settings for collectstatic and is
# removed before the final image is produced.
RUN set -a && . ./ci.env && set +a \
 && python manage.py collectstatic --noinput --no-post-process \
 && rm ci.env

USER dienst2

ENTRYPOINT ["/srv/docker-entrypoint.sh"]
CMD ["gunicorn", "--no-control-socket"]
EXPOSE 8000
