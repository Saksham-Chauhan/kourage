FROM node:16.16.0-slim
WORKDIR /usr/src/app
COPY package*.json ./
ENV TOKEN 
ENV CHANNEL_ID
RUN npm install
COPY . .
RUN node index.js
