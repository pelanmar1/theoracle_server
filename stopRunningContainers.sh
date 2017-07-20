#!/bin/bash

docker stop $(docker ps -aq) > /dev/null
