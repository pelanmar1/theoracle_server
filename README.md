# flasktest

```
docker build -t flask-tutorial:latest .
```

```
docker stop predictapi
docker rm predictapi
docker run -i -p 5000:5000 \
--name predictapi  \
-v /Users/mielliot/Dropbox/mmac/gitent/theoracle:/app/src \
-d flask-tutorial
```

```
docker exec -it predictapi bash
```


```
buildRunCheck.sh - Build the docker image, run it and check that it's running with 'docker ps'
```
