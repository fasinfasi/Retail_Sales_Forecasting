FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# Use serve to run the React build
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]
