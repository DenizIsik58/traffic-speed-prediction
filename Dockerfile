FROM ubuntu:latest

# Make and set the directorties and copy all our files into the docker container
RUN mkdir /app
WORKDIR /app
COPY . .

# Update the packagemanager and add python3 + pip3
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && apt-get install -y postgresql-server-dev-all \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && cd ~ \
  && cd /app

ENV DEBIAN_FRONTEND noninteractive
RUN pip3 install -U scikit-learn
RUN apt update && apt install -y tcl

RUN apt-get update
RUN apt-get install -y python3-numpy python3-scipy python3-matplotlib python3-pandas python3-sympy python3-nose
RUN pip3 install -r requirements.txt
RUN apt-get install -y bash
RUN apt-get install -y build-essential swig python3-dev

# Expose port 8000 for the container
EXPOSE 8000
EXPOSE 6000

# Specify the commands
CMD ["python3", "traffic_speed_prediction/manage.py", "runserver",  "0.0.0.0:8000"]
