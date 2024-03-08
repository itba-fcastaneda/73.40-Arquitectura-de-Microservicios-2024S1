#!/usr/bin/env bash

docker run --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp gcc gcc -o hwc hw.c

docker build -f Dockerfile-libc -t libc .
docker build -t hwc:base .

docker run hwc:base
