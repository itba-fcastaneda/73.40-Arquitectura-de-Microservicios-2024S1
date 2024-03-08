#!/usr/bin/env bash

docker run --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp golang go build -v hw.go

docker build -t hw .

docker run hw
