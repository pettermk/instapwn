FROM python:3.10-alpine

WORKDIR /app
RUN apk add --update --no-cache make libpq postgresql-dev gcc g++ python3-dev musl-dev libffi-dev tzdata jpeg-dev zlib-dev libxml2-dev libxslt-dev
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY instapwn/ instapwn/
WORKDIR /app/instapwn

EXPOSE 8000
