FROM python:3.10-alpine as dev

RUN adduser -D instapwn
USER instapwn
WORKDIR /app
COPY --chown=instapwn:instapwn requirements.txt .
RUN pip install --user -r requirements.txt

ENV PATH="/home/instapwn/.local/bin:${PATH}"

COPY --chown=instapwn:instapwn instapwn/ instapwn/
WORKDIR /app/instapwn

EXPOSE 8000

FROM dev as collectstatic
RUN python manage.py collectstatic --noinput

FROM nginx:alpine as nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY deploy/nginx.conf /etc/nginx/templates/nginx.conf.template
COPY --from=collectstatic /app/instapwn/static/ /app/static/

EXPOSE 80
