#!/bin/bash

IMAGE=bootstrapper:5000/zhanghui/toy

docker build  -f Dockerfile.k8s -t ${IMAGE} . && docker push ${IMAGE} || true


