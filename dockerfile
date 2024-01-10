#syntax=docker/dockerfile:1.3

FROM 944284896973.dkr.ecr.us-east-1.amazonaws.com/cds/python-base-image-3-11:latest as base

FROM base AS build

RUN --mount=type=cache,target=/var/cache/apt apt-get update \
    && apt-get install -y git \
    libssl-dev \
    openssh-client \
    pkg-config

WORKDIR /tmp

ENV PATH=/opt/local/bin:$PATH
ENV PIP_PREFIX=/opt/local
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

COPY requirements.txt .
RUN grep -ivE "psycopg2" requirements.txt > requirements-ex-base.txt
RUN --mount=type=ssh pip install -r requirements-ex-base.txt

###

FROM base AS deploy

COPY --chown=elevatus:elevatus --from=build /opt/local /opt/local
COPY --chown=elevatus:elevatus --from=build /usr/lib/x86_64-linux-gnu/ /lib/x86_64-linux-gnu/ /usr/lib/

WORKDIR /app
COPY --chown=elevatus:elevatus . /app

# DO NOT TOUCH: Gets auto-updated by Ahab on release
ENV APP_VERSION=0.1.0
ENV APP_NAME="subscription-domain-service"

ENV PATH=/opt/local/bin:$PATH \
    PYTHONPATH=/opt/local/lib/python3.11/site-packages:/app/src \
    GUNICORN_CMD_ARGS=$GUNICORN_CMD_ARGS

EXPOSE 8000

STOPSIGNAL SIGINT

USER elevatus:elevatus
CMD [ "gunicorn", "-c", "gunicorn_conf.py", "-b", "0.0.0.0:8000", "src.main:app"]
