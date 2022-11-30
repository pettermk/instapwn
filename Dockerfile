FROM python:3.10-alpine as base

# Add non-root user
RUN adduser -D instapwn
USER instapwn
WORKDIR /app

FROM base as python-builder
# Install build dependencies as root
USER root
RUN apk add --update --no-cache make libpq postgresql-dev gcc g++ python3-dev musl-dev libffi-dev tzdata jpeg-dev zlib-dev libxml2-dev libxslt-dev

# Change to non-root user, create virtualenv and install requirements
USER instapwn
COPY requirements.txt .
RUN python -m venv --copies /app/venv
RUN . /app/venv/bin/activate && pip install -r requirements.txt

FROM python-builder as collectstatic
ENV PATH="/app/venv/bin:${PATH}"
# Copy the application code and collect static files
COPY --chown=instapwn:instapwn instapwn/ instapwn/
WORKDIR /app/instapwn
RUN python manage.py collectstatic --noinput

FROM base as python-runner
# Copy the virtualenv and activate it
COPY --from=python-builder /app/venv/ /app/venv/
RUN . /app/venv/bin/activate

# Copy the application code
COPY --chown=instapwn:instapwn instapwn/ instapwn/
WORKDIR /app/instapwn
ENV PATH="/app/venv/bin:${PATH}"

EXPOSE 8000

FROM nginx:alpine as nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY deploy/nginx.conf /etc/nginx/templates/nginx.conf.template
COPY --from=collectstatic /app/instapwn/static/ /app/static/

EXPOSE 80
