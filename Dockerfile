FROM python:3.10-alpine as dev

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY instapwn/ instapwn/
WORKDIR /app/instapwn

EXPOSE 8000

FROM dev as collectstatic
RUN python manage.py collectstatic --noinput

FROM nginx:alpine as nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY deploy/nginx.conf /etc/nginx/templates/nginx.conf.template
COPY --from=collectstatic /app/instapwn/static/ /app/static/

EXPOSE 80
