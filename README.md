# flasktest


1. Clone de repo.
2. Run 

sh fastSetup.sh [path_to_theoracle_dir] [path_to_flasktest_dir]

For Web App:

open the file flasktest/web_app/home/home.html


<!-- 
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
    -v /Users/mielliot/Dropbox/mmac/gitent/flasktest/scripts:/app/scripts \
    -v /Users/mielliot/Dropbox/mmac/gitent/flasktest/conf:/var/conf \
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
``` -->


TODO LIST

Remove all tmp files over an hour old in the cron job
Change the tmp file naming scheme to something uniq so files dont collide
Need a way to clean up requests that cause train.py to crash
Get LinearReg and PyFlux working again
