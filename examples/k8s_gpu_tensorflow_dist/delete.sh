#!/bin/bash
kubectl delete ConfigMap tensorflow-cluster-config
kubectl delete job tensorflow-ps-rc tensorflow-worker0-rc tensorflow-worker1-rc tensorflow-worker2-rc
kubectl delete service tensorflow-ps-service tensorflow-wk-service0 tensorflow-wk-service1
