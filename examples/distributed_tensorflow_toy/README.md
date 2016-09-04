# A toy example of distributed tensorflow

## Requirements:
* Nvidia driver libraries in the directory `/var/lib/nvidia` on host node
* mount the NFS/CephFS to the same directory (e.g. /mnt/cephfs) on each node

## Build the image
```
docker build -t dtf .
```
在 Dockefile 中，基于 10.10.10.94:5000/tensorflow:0.9.0-gpu 创建 dtf 测试 images，创建 example 文件夹，并将 toy.py 复制到镜像中供测试。

## Test Guide：
* 使用 10.10.10.94 和 10.10.10.191 两台带有 GPUs 的节点测试。
* 两个节点分别担当 worker 和 ps 角色。
* 在 worker 上执行线性拟合的实验估计拟合的权重和 offset，迭代次数10次。

## Start parameter server:
在 10.10.10.94 上启动：
```
docker run --net=host --privileged -v /var/lib/nvidia:/usr/local/nvidia/lib64 -v /mnt/cephfs:/mnt/cephfs -it dtf /bin/bash
```

在 docker container 中启动 toy.py，设置 `--job_name=ps` 和 `--task_index=0`：
```
python toy.py  --ps_hosts=10.10.10.94:2222  --worker_hosts=10.10.10.191:2222 --job_name=ps --task_index=0
```
部分输出结果：
```
I tensorflow/core/common_runtime/gpu/gpu_init.cc:126] DMA: 0 1 2 3 4 5 6 7
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 0:   Y Y Y Y N N N N
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 1:   Y Y Y Y N N N N
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 2:   Y Y Y Y N N N N
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 3:   Y Y Y Y N N N N
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 4:   N N N N Y Y Y Y
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 5:   N N N N Y Y Y Y
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 6:   N N N N Y Y Y Y
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 7:   N N N N Y Y Y Y
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce GTX TITAN X, pci bus id: 0000:04:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:1) -> (device: 1, name: GeForce GTX TITAN X, pci bus id: 0000:05:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:2) -> (device: 2, name: GeForce GTX TITAN X, pci bus id: 0000:08:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:3) -> (device: 3, name: GeForce GTX TITAN X, pci bus id: 0000:09:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:4) -> (device: 4, name: GeForce GTX TITAN X, pci bus id: 0000:84:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:5) -> (device: 5, name: GeForce GTX TITAN X, pci bus id: 0000:85:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:6) -> (device: 6, name: GeForce GTX TITAN X, pci bus id: 0000:88:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:7) -> (device: 7, name: GeForce GTX TITAN X, pci bus id: 0000:89:00.0)
I tensorflow/core/distributed_runtime/rpc/grpc_channel.cc:206] Initialize HostPortsGrpcChannelCache for job ps -> {localhost:2222}
I tensorflow/core/distributed_runtime/rpc/grpc_channel.cc:206] Initialize HostPortsGrpcChannelCache for job worker -> {10.10.10.191:2222}
I tensorflow/core/distributed_runtime/rpc/grpc_server_lib.cc:202] Started server with target: grpc://localhost:2222
```

## Start worker:
在 10.10.10.191 上启动：
```
docker run --net=host --privileged -v /var/lib/nvidia:/usr/local/nvidia/lib64 -v /mnt/cephfs:/mnt/cephfs -it dtf /bin/bash
```

在 docker container 中启动 toy.py，设置 `--job_name=worker` 和 `--task_index=0`：
```
python toy.py  --ps_hosts=10.10.10.94:2222  --worker_hosts=10.10.10.191:2222 --job_name=worker --task_index=0
```

部分输出结果：
```
I tensorflow/core/common_runtime/gpu/gpu_init.cc:126] DMA: 0 1 2 3
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 0:   Y Y Y Y
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 1:   Y Y Y Y
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 2:   Y Y Y Y
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 3:   Y Y Y Y
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce GTX 980, pci bus id: 0000:04:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:1) -> (device: 1, name: GeForce GTX 980, pci bus id: 0000:05:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:2) -> (device: 2, name: GeForce GTX 980, pci bus id: 0000:08:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:3) -> (device: 3, name: GeForce GTX 980, pci bus id: 0000:09:00.0)
I tensorflow/core/distributed_runtime/rpc/grpc_channel.cc:206] Initialize HostPortsGrpcChannelCache for job ps -> {10.10.10.94:2222}
I tensorflow/core/distributed_runtime/rpc/grpc_channel.cc:206] Initialize HostPortsGrpcChannelCache for job worker -> {localhost:2222}
I tensorflow/core/distributed_runtime/rpc/grpc_server_lib.cc:202] Started server with target: grpc://localhost:2222
=========> step: 0
-0.863596
9.73686
=========> step: 1
0.318785
10.474
=========> step: 2
1.12191
10.315
=========> step: 3
1.55386
10.1671
=========> step: 4
1.77544
10.0838
=========> step: 5
1.88783
10.0406
=========> step: 6
1.94467
10.0187
=========> step: 7
1.9734
10.0076
=========> step: 8
1.98791
10.0019
=========> step: 9
1.99525
9.99909
```

迭代 10 次后，权重和 offset 分别逼近 2 和 10。

参考：
* https://github.com/tensorflow/tensorflow/blob/master/tensorflow/g3doc/how_tos/distributed/index.md
* https://www.tensorflow.org/versions/master/how_tos/distributed/index.html
* http://weibo.com/ttarticle/p/show?id=2309403988813608274928
* http://weibo.com/ttarticle/p/show?id=2309403987407065210809
