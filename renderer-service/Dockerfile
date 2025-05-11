FROM node:18

WORKDIR /app

COPY package.json .
RUN npm install

RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libxfixes3 \
    libxtst6 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    fonts-liberation \
    fonts-noto-color-emoji

COPY server.js .

EXPOSE 3000

CMD ["npm", "start"]