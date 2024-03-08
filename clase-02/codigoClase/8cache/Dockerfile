FROM ubuntu:latest

RUN apt-get update && apt-get install -y gcc make
COPY main.c Makefile /src/
WORKDIR /src/
RUN make build
