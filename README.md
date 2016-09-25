# k8s-tensorflow
本文档介绍如何在 Kubernetes 集群中运行 GPU 版 Tensorflow 任务，主要包括：

## 配置集群节点 GPU
* [build GPU drivers](build_gpu_drivers)
* [load GPU drivers](load_gpu_drivers)

docker GPU 示例包括：
* [gpu_docker_tensorflow_mat_multi](examples/gpu_docker_tensorflow_mat_multi)
* [distributed_tensorflow_toy](examples/distributed_tensorflow_toy)
* [mnist](examples/mnist)


## 配置 k8s 使用 GPU
* [build k8s with multi-GPUs support](build_k8s)

示例包括：

* [k8s with multi-GPUs](examples/k8s_multigpu)

## k8s + GPU distributed Tensorflow

示例包括：

* k8s with multi-GPUs mnist

## 附加实验：

* k8s 使用 Ceph 作为 persistent volume
* Run CPU distributed Tensorflow on k8s
