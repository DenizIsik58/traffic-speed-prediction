FROM node:16-alpine

# Make and set the directorties and copy all our files into the docker container
RUN mkdir /app
WORKDIR /app
COPY . .

# Update the packagemanager and add python3 + pip3
RUN apk add --update
RUN apk add python3
RUN python3 -m ensurepip

RUN pip3 install pip --upgrade


RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

RUN pip3 install -r requirements.txt

# Expose port 8000 for the container
EXPOSE 8000
EXPOSE 5432

# Specify the commands
CMD ["StartApplication.ps1"]
