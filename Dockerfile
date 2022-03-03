FROM node:16-alpine


RUN mkdir /app
WORKDIR /app
COPY . /app


RUN apk add --update
RUN apk add python3
RUN python3 -m ensurepip

RUN npm install webpack webpack-cli --save-dev
RUN npm install @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev

RUN pip3 install pip --upgrade
RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["app/traffic_speed_prediction/manage.py runserver"]