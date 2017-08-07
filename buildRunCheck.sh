#!/bin/bash

docker build -t predictapi:latest .
docker stop predictapi
docker rm predictapi
docker run -i -p 5000:5000 \
	--name predictapi  \
	-v /Users/t-pelanz/Documents/Microsoft/theoracle:/app/src \
	-d predictapi

#sleep 1s # this is used because when containers don't work they quit after 1 sec and don't show up on docker ps
#docker ps

exit 0

'


'