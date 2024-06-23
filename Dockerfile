FROM python:3.12.4
# docker run --rm -it -v `pwd`:/usr/src/app -w /usr/src/app python:3.12.4 bash

ENV LANG en_GB.UTF-8

# TODO create a user account and use it install Python modules and run the app.

WORKDIR /usr/src/app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt
