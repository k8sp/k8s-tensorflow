#!/bin/bash

set -xe

IMAGE=bootstrapper:5000/zhanghui/tensorflow-test:1.1.0-gpu

docker build -t ${IMAGE} -f Dockerfile.k8s . && docker push ${IMAGE}

kubectl create -f .
