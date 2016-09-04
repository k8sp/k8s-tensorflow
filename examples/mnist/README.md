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

## Test Guide:
* 使用 10.10.10.94 和 10.10.10.191 两台带有 GPUs 的节点测试。
* 两个节点分别担当 worker 和 ps 角色。

## Start parameter server:
在 10.10.10.94 上启动：
```
docker run --net=host --privileged \
-v /var/lib/nvidia:/usr/local/nvidia/lib64 \
-v /mnt/cephfs:/mnt/cephfs -it 10.10.10.94:5000/mnist /bin/bash
```

在 docker container 中启动 mnist.py，设置 `--job_name=ps` 和 `--task_index=0`：
```
python mnist.py  \
--ps_hosts=10.10.10.94:2222  --worker_hosts=10.10.10.191:2222 \
--job_name=ps --task_index=0
```
部分输出结果：
```
...
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
docker run --net=host --privileged \
-v /var/lib/nvidia:/usr/local/nvidia/lib64 \
-v /mnt/cephfs:/mnt/cephfs -it 10.10.10.94:5000/mnist /bin/bash
```

在 docker container 中启动 mnist.py，设置 `--job_name=worker` 和 `--task_index=0`：
```
python mnist.py  \
--ps_hosts=10.10.10.94:2222  --worker_hosts=10.10.10.191:2222 \
--job_name=worker --task_index=0
```

部分输出结果：
```
...
Step: 8900,  Epoch: 17,  Batch: 100 of 550,  Cost: 4.0152,  AvgTime: 59.39ms
Step: 9000,  Epoch: 17,  Batch: 200 of 550,  Cost: 4.0853,  AvgTime: 31.43ms
Step: 9100,  Epoch: 17,  Batch: 300 of 550,  Cost: 3.5491,  AvgTime: 48.64ms
Step: 9200,  Epoch: 17,  Batch: 400 of 550,  Cost: 3.4796,  AvgTime: 56.23ms
Step: 9300,  Epoch: 17,  Batch: 500 of 550,  Cost: 3.5904,  AvgTime: 46.35ms
Step: 9350,  Epoch: 17,  Batch: 550 of 550,  Cost: 4.1797,  AvgTime: 29.90ms
Step: 9450,  Epoch: 18,  Batch: 100 of 550,  Cost: 3.7226,  AvgTime: 47.45ms
Step: 9550,  Epoch: 18,  Batch: 200 of 550,  Cost: 3.6964,  AvgTime: 45.49ms
Step: 9650,  Epoch: 18,  Batch: 300 of 550,  Cost: 4.1049,  AvgTime: 43.18ms
Step: 9750,  Epoch: 18,  Batch: 400 of 550,  Cost: 4.0978,  AvgTime: 41.52ms
Step: 9850,  Epoch: 18,  Batch: 500 of 550,  Cost: 3.7147,  AvgTime: 54.74ms
Step: 9900,  Epoch: 18,  Batch: 550 of 550,  Cost: 3.4491,  AvgTime: 15.36ms
Step: 10000,  Epoch: 19,  Batch: 100 of 550,  Cost: 3.9483,  AvgTime: 49.24ms
Step: 10100,  Epoch: 19,  Batch: 200 of 550,  Cost: 3.9788,  AvgTime: 54.67ms
Step: 10200,  Epoch: 19,  Batch: 300 of 550,  Cost: 3.6887,  AvgTime: 62.02ms
Step: 10300,  Epoch: 19,  Batch: 400 of 550,  Cost: 3.5539,  AvgTime: 53.69ms
Step: 10400,  Epoch: 19,  Batch: 500 of 550,  Cost: 3.6966,  AvgTime: 38.00ms
Step: 10450,  Epoch: 19,  Batch: 550 of 550,  Cost: 3.8850,  AvgTime: 13.11ms
Step: 10550,  Epoch: 20,  Batch: 100 of 550,  Cost: 3.1706,  AvgTime: 46.13ms
Step: 10650,  Epoch: 20,  Batch: 200 of 550,  Cost: 3.3553,  AvgTime: 50.18ms
Step: 10750,  Epoch: 20,  Batch: 300 of 550,  Cost: 3.5253,  AvgTime: 31.43ms
Step: 10850,  Epoch: 20,  Batch: 400 of 550,  Cost: 3.8232,  AvgTime: 44.60ms
Step: 10950,  Epoch: 20,  Batch: 500 of 550,  Cost: 3.6269,  AvgTime: 33.73ms
Step: 11000,  Epoch: 20,  Batch: 550 of 550,  Cost: 3.3322,  AvgTime: 25.31ms
Test-Accuracy: 0.28
Total Time: 537.31s
Final Cost: 3.3322
done
```


## References
* http://ischlag.github.io/2016/06/12/async-distributed-tensorflow
* https://github.com/ischlag/distributed-tensorflow-example
