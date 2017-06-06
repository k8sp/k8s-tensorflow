#!/bin/bash

set -xe

IMAGE="bootstrapper:5000/zhanghui/tensorflow-test"

docker build --no-cache=false -t ${IMAGE} -f Dockerfile.k8s . && docker push ${IMAGE}

kubectl delete -f . || true
sleep 3
kubectl create -f . || true
