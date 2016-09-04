# A distributed tensorflow MNIST example

## Requirements:
* Nvidia driver libraries in the directory `/var/lib/nvidia` on host node
* mount the NFS/CephFS to the same directory (e.g. /mnt/cephfs) on each node

## Build the image:
```
docker build -t mnist .
```
在 Dockefile 中，基于 10.10.10.94:5000/tensorflow:0.9.0-gpu 创建 mnist 测试 images，创建 example 文件夹，并将 mnist.py 和 MNIST_data 复制到镜像中供测试。

上传至私有 docker registry, 方便其他机器下载测试：
```
docker tag mnist 10.10.10.94:5000/mnist
docker push 10.10.10.94:5000/mnist
```

## User Guide:
* 使用 10.10.10.93,10.10.10.94 和 10.10.10.191 带有 GPUs 的节点测试。
* 10.10.10.93,10.10.10.94 两个节点分别担当 worker,对应 `task_index=0` 和 `task_index=1`。
* 10.10.10.191 担当 ps,对应 `task_index=0`。

## Start parameter server:
在 10.10.10.191 上启动：
```
docker run --net=host --privileged \
-v /var/lib/nvidia:/usr/local/nvidia/lib64 \
-v /mnt/cephfs:/mnt/cephfs -it 10.10.10.94:5000/mnist /bin/bash
```

在 docker container 中启动 mnist.py，设置 `--job_name=ps` 和 `--task_index=0`：
```
python mnist.py  \
--ps_hosts=10.10.10.191:2222 --worker_hosts=10.10.10.93:2222,10.10.10.94:2222 \
--job_name=ps --task_index=0
```
部分输出结果：
```
...
I tensorflow/core/common_runtime/gpu/gpu_init.cc:126] DMA: 0 1 2 3
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 0:   Y Y Y Y
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 1:   Y Y Y Y
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 2:   Y Y Y Y
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 3:   Y Y Y Y
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce GTX 980, pci bus id: 0000:04:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:1) -> (device: 1, name: GeForce GTX 980, pci bus id: 0000:05:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:2) -> (device: 2, name: GeForce GTX 980, pci bus id: 0000:08:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:3) -> (device: 3, name: GeForce GTX 980, pci bus id: 0000:09:00.0)
I tensorflow/core/distributed_runtime/rpc/grpc_channel.cc:206] Initialize HostPortsGrpcChannelCache for job ps -> {localhost:2222}
I tensorflow/core/distributed_runtime/rpc/grpc_channel.cc:206] Initialize HostPortsGrpcChannelCache for job worker -> {10.10.10.93:2222, 10.10.10.94:2222}
I tensorflow/core/distributed_runtime/rpc/grpc_server_lib.cc:202] Started server with target: grpc://localhost:2222
```

## Start worker:

在 10.10.10.93 上启动：
```
docker run --net=host --privileged \
-v /var/lib/nvidia:/usr/local/nvidia/lib64 \
-v /mnt/cephfs:/mnt/cephfs -it 10.10.10.94:5000/mnist /bin/bash
```

在 docker container 中启动 mnist.py，设置 `--job_name=worker` 和 `--task_index=0`：
```
python mnist.py  \
--ps_hosts=10.10.10.191:2222 --worker_hosts=10.10.10.93:2222,10.10.10.94:2222 \
--job_name=worker --task_index=0
```

在 10.10.10.94 上启动：
```
docker run --net=host --privileged \
-v /var/lib/nvidia:/usr/local/nvidia/lib64 \
-v /mnt/cephfs:/mnt/cephfs -it 10.10.10.94:5000/mnist /bin/bash
```

在 docker container 中启动 mnist.py，设置 `--job_name=worker` 和 `--task_index=1`：
```
python mnist.py  \
--ps_hosts=10.10.10.191:2222 --worker_hosts=10.10.10.93:2222,10.10.10.94:2222 \
--job_name=worker --task_index=1
```

部分输出结果：
```
...
Step: 21400,  Epoch: 19,  Batch: 500 of 550,  Cost: 2.5811,  AvgTime: 67.64ms
Step: 21450,  Epoch: 19,  Batch: 550 of 550,  Cost: 2.2504,  AvgTime: 33.72ms
Step: 21550,  Epoch: 20,  Batch: 100 of 550,  Cost: 2.6379,  AvgTime: 100.74ms
Step: 21650,  Epoch: 20,  Batch: 200 of 550,  Cost: 2.4363,  AvgTime: 98.42ms
Step: 21750,  Epoch: 20,  Batch: 300 of 550,  Cost: 2.6610,  AvgTime: 75.29ms
Step: 21850,  Epoch: 20,  Batch: 400 of 550,  Cost: 3.1111,  AvgTime: 82.97ms
Step: 21950,  Epoch: 20,  Batch: 500 of 550,  Cost: 2.4441,  AvgTime: 64.84ms
Step: 22000,  Epoch: 20,  Batch: 550 of 550,  Cost: 2.7931,  AvgTime: 33.21ms
Test-Accuracy: 0.42
Total Time: 825.44s
Final Cost: 2.7931
done
```

```
...
Step: 16632,  Epoch: 19,  Batch: 400 of 550,  Cost: 2.8109,  AvgTime: 48.77ms
Step: 16807,  Epoch: 19,  Batch: 500 of 550,  Cost: 3.5114,  AvgTime: 47.59ms
Step: 16907,  Epoch: 19,  Batch: 550 of 550,  Cost: 2.8528,  AvgTime: 31.16ms
Step: 17071,  Epoch: 20,  Batch: 100 of 550,  Cost: 3.1005,  AvgTime: 48.23ms
Step: 17237,  Epoch: 20,  Batch: 200 of 550,  Cost: 2.5541,  AvgTime: 50.43ms
Step: 17380,  Epoch: 20,  Batch: 300 of 550,  Cost: 3.2043,  AvgTime: 36.57ms
Step: 17567,  Epoch: 20,  Batch: 400 of 550,  Cost: 3.2265,  AvgTime: 64.14ms
Step: 17747,  Epoch: 20,  Batch: 500 of 550,  Cost: 2.5211,  AvgTime: 57.14ms
Step: 17851,  Epoch: 20,  Batch: 550 of 550,  Cost: 3.0061,  AvgTime: 37.45ms
Test-Accuracy: 0.37
Total Time: 565.77s
Final Cost: 3.0061
done
```

## References
* http://ischlag.github.io/2016/06/12/async-distributed-tensorflow
* https://github.com/ischlag/distributed-tensorflow-example
