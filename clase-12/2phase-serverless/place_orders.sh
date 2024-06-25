#!/bin/bash

for i in {1..1000}
do
    for j in {1..5}
    do
	curl -X GET $1/default
	echo " - $i - $j"
    done
    sleep 1
done
