docker stop jamescontainer
docker rm jamescontainer
docker build -t jamesfasttest .
docker run -itd --name jamescontainer -p 9090:9090 jamesfasttest