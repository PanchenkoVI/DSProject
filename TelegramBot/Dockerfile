FROM node:16-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci
# RUN npm i -D nodemon cross-env
# RUN npm i telegraf config
# RUN npm install csv-parser
RUN npm i axios fluent-ffmpeg @ffmpeg-installer/ffmpeg
# RUN npm install openai

COPY . .

ENV PORT=3000

EXPOSE $PORT

CMD [ "npm", "start" ]