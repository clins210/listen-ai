# stat/Dockerfile
FROM golang:1.23-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o stat .

# 用更輕量的 image 跑
FROM alpine:latest

WORKDIR /app
COPY --from=builder /app/stat .

ENV STAT_PORT=8002
ENV SQLITE_PATH=/data/listenai.db

EXPOSE 8002

CMD ["./stat"]