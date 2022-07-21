# pull official base image
FROM python:3.8.1-alpine

# install dependencies
# updated
RUN apk update && \
    apk add --no-cache --virtual build-deps \
    openssl-dev libffi-dev g++ python3-dev musl-dev \
    postgresql-dev netcat-openbsd bind-tools 

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set working directory
WORKDIR /usr/src/tradelytics

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/tradelytics/requirements.txt
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/tradelytics/entrypoint.sh
RUN chmod +x /usr/src/tradelytics/entrypoint.sh
COPY ./entrypoint.sh /usr/src/tradelytics/entrypoint-data.sh
RUN chmod +x /usr/src/tradelytics/entrypoint-data.sh

# add app
COPY . /usr/src/tradelytics
