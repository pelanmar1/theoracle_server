#!/bin/bash

PATH=/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

for i in {1..1};
do
	now=$(date +"%T")
	echo ""
    echo "Time : $now"
	python3 /app/scripts/train.py
done
