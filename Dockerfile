# base image
FROM python:3
# setup environment variable
ENV DockerHOME=/home/app

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME
# copy whole project to your docker home directory.
COPY . $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip


# run this command to install all dependencies
RUN pip install -r requirements.txt
