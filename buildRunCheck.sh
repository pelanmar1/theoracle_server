#!/bin/bash

# Uncomment if first time
docker build -t predictapi:latest .


docker stop predictapi
docker rm predictapi
docker run -i -p 5000:5000 \
	--name predictapi  \
	-v /Users/t-pelanz/Documents/Microsoft/theoracle:/app/src \
    -v /Users/t-pelanz/Documents/Microsoft/flasktest/app:/app/app \
    -v /Users/t-pelanz/Documents/Microsoft/flasktest/data:/app/data \
    -v /Users/t-pelanz/Documents/Microsoft/flasktest/scripts:/app/scripts \
    -v /Users/t-pelanz/Documents/Microsoft/flasktest/conf:/var/conf \
    -v /Users/t-pelanz/Documents/Microsoft/flasktest/web:/app/web \
	-d predictapi


exit 0

