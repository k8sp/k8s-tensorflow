#!/bin/bash
kubectl create -f worker_ps_service_GPU.yaml
kubectl create -f worker_ps_rc_GPU.yaml
