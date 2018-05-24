FROM python:3-alpine
ENV PYTHONUNBUFFERED 1
ENV HTTP_PROXY "http://10.10.16.8:3128"
ENV HTTPS_PROXY "http://10.10.16.8:3128"
RUN apk update && apk add --no-cache build-base python-dev py-pip jpeg-dev zlib-dev libpq postgresql-dev
ENV LIBRARY_PATH=/lib:/usr/lib
RUN mkdir /code
WORKDIR /code
ADD backend/requirements.txt /code/
RUN pip --proxy http://10.10.16.8:3128 install -r requirements.txt
ADD ./backend /code/