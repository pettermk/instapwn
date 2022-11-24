FROM python:3.10-alpine as base

RUN adduser -D instapwn
USER instapwn
WORKDIR /app

FROM base as python-builder
USER root
RUN apk add --update --no-cache make libpq postgresql-dev gcc g++ python3-dev musl-dev libffi-dev tzdata jpeg-dev zlib-dev libxml2-dev libxslt-dev
COPY --chown=instapwn:instapwn requirements.txt .
RUN python -m venv --copies /app/venv
RUN . /app/venv/bin/activate && pip install -r requirements.txt

COPY --chown=instapwn:instapwn instapwn/ instapwn/
WORKDIR /app/instapwn

FROM python-builder as collectstatic
WORKDIR /app/instapwn
USER root
ENV PATH="/app/venv/bin:${PATH}"
RUN python manage.py collectstatic --noinput

FROM base as python-runner
USER instapwn
COPY --from=python-builder --chown=instapwn:instapwn /app/venv/ /app/venv/
WORKDIR /app/instapwn
RUN . /app/venv/bin/activate
ENV PATH="/app/venv/bin:${PATH}"
COPY --chown=instapwn:instapwn instapwn/ .

EXPOSE 8000


FROM nginx:alpine as nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY deploy/nginx.conf /etc/nginx/templates/nginx.conf.template
COPY --from=collectstatic /app/instapwn/static/ /app/static/

EXPOSE 80
