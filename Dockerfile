FROM python:3.8

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY instapwn/ instapwn/
WORKDIR /app/instapwn

EXPOSE 8000
