FROM node:16-alpine

RUN apk add --update --no-cache tzdata

WORKDIR /frontend
COPY package.json ./

ENV NODE_ENV=production
ARG NODE_ENV=production


RUN npm install -g npm@8.7.0
RUN npm install -g serve
RUN npm install --force

COPY .. .

EXPOSE 3000

CMD [ "serve", "-s" , "build" ]
