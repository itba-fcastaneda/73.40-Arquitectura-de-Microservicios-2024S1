#!/usr/bin/env bash

docker run --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp gcc gcc -o hwc hw.c

docker build -t hwc:ubuntu .

docker run hwc:ubuntu
