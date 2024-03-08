#!/usr/bin/env bash

docker run --rm -v "$PWD":/app -w /app gcc gcc -std=c99 -o args args.c

docker build -t args .

docker run args $*
