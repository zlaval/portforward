FROM python:3.9.13-slim-buster

WORKDIR /usr/src/app

COPY main.py ./

CMD [ "python", "./main.py" ]
