FROM node:16-alpine

RUN apk add --update --no-cache tzdata

WORKDIR /frontend
COPY package.json ./


RUN npm install -g npm@8.7.0
RUN npm install --force

COPY .. .

EXPOSE 3000

CMD [ "npm", "start" ]