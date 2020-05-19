FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get -y install cmake
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN mkdir /code
WORKDIR /code
COPY . /code/
