#!/bin/bash

programname=$0

echo "Usage: $programname [path_to_theoracle_dir] [path_to_flasktest_dir]"

# Defaults
PATH_ORACLE="/Users/t-pelanz/Documents/Microsoft/theoracle"
PATH_FLASK="/Users/t-pelanz/Documents/Microsoft/flasktest"


# Set up paths to theOracle and Flasktest if given
if (( "$#" == 2 )) 
then
    PATH_ORACLE="$1"
    PATH_FLASK="$2"
fi

# If image not already built, build it.

img=$(docker images -q predictapi)

if [[ ! -n "$img" ]]; then
    echo "Building image..."
    docker build -t predictapi:latest .
else
    echo "Image already built."
fi

# stop running container if exists
echo "Checking if container is already running."
cont=$(docker ps  --filter="name=predictapi" -aq)
if ! [[ -z $cont ]]; then
    docker stop predictapi
    docker rm predictapi
    echo "Stoping current running instance."
fi

# run container
echo "Running new instance"
docker run -i -p 5000:5000 \
	--name predictapi  \
	-v $PATH_ORACLE":/app/src" \
    -v $PATH_FLASK"/app:/app/app" \
    -v $PATH_FLASK"/data:/app/data" \
    -v $PATH_FLASK"/scripts:/app/scripts" \
    -v $PATH_FLASK"/conf:/var/conf" \
    -v $PATH_FLASK"/web_app:/app/web_app" \
	-d predictapi


exit 0