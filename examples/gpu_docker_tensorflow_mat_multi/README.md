# GPU Docker based TensorFlow Matrix Multiplication

## Requirements:
* Nvidia drivers in the directory `/var/lib/nvidia` on host node

## Usage:
```
$ docker build -t gpu_docker_tf_mat_multi .
$ docker run -it  --privileged -v /var/lib/nvidia:/usr/local/nvidia/lib64 gpu_docker_tf_mat_multi
```

