FROM node:16

WORKDIR /docs

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# Deployment step


# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
