FROM node:16

WORKDIR /app

EXPOSE 3001

COPY package.json ./

RUN npm install

COPY . /app/

RUN npm install -g typescript
RUN tsc