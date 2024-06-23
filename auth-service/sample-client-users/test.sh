#!/bin/bash

curl -X DELETE api:5000/ping
curl -X POST api:5000/ping


# npm test
echo "NPM TEST"
