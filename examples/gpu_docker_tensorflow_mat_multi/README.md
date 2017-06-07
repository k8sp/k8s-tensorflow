# GPU Docker based TensorFlow Matrix Multiplication

Using a single GPU on a multi-GPU system

## Requirements:
* Nvidia drivers in the directory `/var/lib/nvidia` on host node

## Usage:
```
$ docker build -t gpu_docker_tf_mat_multi .
$ docker run -it  --privileged -v /var/lib/nvidia:/usr/local/nvidia/lib64 gpu_docker_tf_mat_multi
```

* `--privileged` makes the docker container can access the GPUs on host node
* `-v /var/lib/nvidia:/usr/local/nvidia/lib64` map the Nvidia dynamic libraries on host to docker container


## Node Affinity 

* [Scheduling GPUs](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/)
* [Assigning Pods to Nodes](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/)
* [affinity exmaples](https://github.com/kubernetes/kubernetes.github.io/tree/master/docs/user-guide/node-selection)

## reference

[Using GPUs](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/docs_src/tutorials/using_gpu.md)


