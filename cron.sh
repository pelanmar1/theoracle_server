#!/bin/bash

for i in {1..58};
do
	python3 /app/src/train.py
	sleep 1
done
