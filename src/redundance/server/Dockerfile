FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
COPY tsconfig.json ./
COPY index.ts ./

RUN npm install

RUN npx tsc

CMD ["node", "index.js"]
