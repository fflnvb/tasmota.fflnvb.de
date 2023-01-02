FROM alpine:latest

WORKDIR /app

COPY ./frontend/ ./frontend/
COPY ./backend/ ./backend/

COPY ./frontend/.env ./frontend/.env
COPY .env .env

RUN apk add --no-cache bash
RUN apk add --no-cache python3 py3-pip
RUN apk add --no-cache nodejs npm

RUN cd backend && pip install -r requirements.txt

RUN cd frontend && npm install && npm run build
RUN npm install -g http-server

EXPOSE 8080
EXPOSE 8081

CMD ["bash", "-c", "python /app/backend/__main__.py & http-server /app/frontend/dist "]
