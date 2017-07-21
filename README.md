# flasktest

```
docker build -t flask-tutorial:latest .
```

```
docker stop predictapi
docker rm predictapi
docker run -i -p 5000:5000 \
    --init \
    --name predictapi  \
    -v /Users/mielliot/Dropbox/mmac/gitent/theoracle:/app/src \
    -v /Users/mielliot/Dropbox/mmac/gitent/flasktest/app:/app/app \
    -v /Users/mielliot/Dropbox/mmac/gitent/flasktest/data:/app/data \
    -d flask-tutorial
```

```
docker exec -it predictapi bash
```


```
buildRunCheck.sh - Build the docker image, run it and check that it's running with 'docker ps'
```

```
POST command with curl:

curl -X POST -F "file=@/path/to/file" localhost:5000
```
