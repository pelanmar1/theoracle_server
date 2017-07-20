#!/bin/bash

docker build -t flask-tutorial:latest .
docker stop predictapi
docker rm predictapi
docker run -i -p 5000:5000 \
	--name predictapi  \
	-v /Users/t-daguer/Documents/theoracle:/app/src \
	-d flask-tutorial

#sleep 1s # this is used because when containers don't work they quit after 1 sec and don't show up on docker ps
#docker ps

exit 0
