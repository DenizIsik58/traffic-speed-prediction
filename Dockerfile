FROM node:16-alpine

# Make and set the directorties and copy all our files into the docker container
RUN mkdir /app
WORKDIR /app
COPY . /app

# Update the packagemanager and add python3 + pip3
RUN apk add --update
RUN apk add python3
RUN python3 -m ensurepip

# Install necessary dependencies to run the project
RUN npm init -y
RUN npm install webpack webpack-cli --save-dev
RUN npm install @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev
RUN npm install react react-dom --save-dev
RUN npm install @material-ui/core
RUN npm install @babel/plugin-proposal-class-properties
RUN npm install react-router-dom
RUN npm install @material-ui/icons


RUN pip3 install pip --upgrade
RUN pip3 install -r requirements.txt

# Expose port 8000 for the container
EXPOSE 8000

# Specify the commands
CMD ["python3"]