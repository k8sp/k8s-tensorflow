#!/bin/bash

set -x 

#docker run -it --rm -v $PWD:/tmp bootstrapper:5000/zhanghui/tensorflow:v1.1.0-gpu /bin/bash

docker build -t bootstrapper:5000/zhanghui/tf-gpu-test .
docker push bootstrapper:5000/zhanghui/tf-gpu-test

kubectl create -f gputest_volume.yaml
