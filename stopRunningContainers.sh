#!/bin/bash

docker stop $(docker ps -aq) > /dev/null
docker rm $(docker ps -aq) > /dev/null
