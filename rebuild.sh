docker stop jamesfastapi
docker rm jamesfastapi
docker build -t jamesimage .
docker run -itd --name jamesfastapi -p 9090:9090 jamesimage
