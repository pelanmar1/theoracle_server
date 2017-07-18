#!/bin/bash

IMG_NAME=pred-service

USAGE="Usage: buildRunCheck.sh [-img_name IMGNAME]"

while [[ "$#" -gt 1 ]]
do
	arg="$1"
	case $arg in
	-img_name)
		IMG_NAME="$2"
		shift
		;;
	-u|-usage)
		echo $USAGE
		exit 1
		;;
	esac
	shift
done

docker build -t $IMG_NAME:latest .
docker run -d -p 5000:5000 $IMG_NAME
docker ps

exit 0
