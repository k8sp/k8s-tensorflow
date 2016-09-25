# Kubernetes with multi-GPUs
## Requirements:
* 集群 GPU 驱动已加载， GPU 工作正常
* Kubernetes 的主线版本（到目前为止为 v1.3.7）对 GPU 的调度支持不完善，本示例采用 https://github.com/kubernetes/kubernetes/pull/28216 提交的完善对 GPU 支持的 Kubernetes 版本（估计会在 v1.5.0 之后 merge 到 Kubernetes 主线版本），如何编译 Kubernetes 请参考 [build_k8s](../../build_k8s)
* 使用编译后的 Kubernetes 集群工作正常

## 测试一
* 构建测试用 docker image

  在 `gputest.yaml` 中使用的 docker image 是 `10.10.10.94:5000/mnist`, 构建参考 [mnist](../mnist)
* 创建测试 pod

  在 `gputest.yaml` 中指定使用两个 GPUs 资源：
  ```
  resources:
    limits:
      alpha.kubernetes.io/nvidia-gpu: 2
  ```
  创建 pod：
  ```
  kubectl create -f gputest.yaml
  ```
* 查看 pod 信息

  ```
  $ kubectl get po -o wide
  NAME               READY     STATUS    RESTARTS   AGE       IP          NODE
  nvidia-gpu-test2   1/1       Running   0          2h        10.1.81.2   10.10.10.93
  ```
  pod 正常启动，并调度到 10.10.10.93 节点上。
  describe pod:
```
$ kubectl describe po nvidia-gpu-test2
Name:           nvidia-gpu-test2
Namespace:      default
Node:           10.10.10.93/10.10.10.93
Start Time:     Sun, 25 Sep 2016 10:52:58 +0800
Labels:         <none>
Status:         Running
IP:             10.1.81.2
Controllers:    <none>
Containers:
  nvidia-gpu:
    Container ID:       docker://fb4d055e0f1141732f3e1936502e1d5ca83d56754ee4576f3362e54603779205
    Image:              10.10.10.94:5000/mnist
    Image ID:           docker://sha256:fc119928f1afa4f97c18839431cace61b58bcbad4a54da6f223ffb0d8a1fb635
    Port:
    Limits:
      alpha.kubernetes.io/nvidia-gpu:   2
    Requests:
      alpha.kubernetes.io/nvidia-gpu:   2
    State:                              Running
      Started:                          Sun, 25 Sep 2016 10:52:59 +0800
    Ready:                              True
    Restart Count:                      0
    Volume Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-q3u80 (ro)
    Environment Variables:      <none>
Conditions:
  Type          Status
  Initialized   True
  Ready         True
  PodScheduled  True
Volumes:
  default-token-q3u80:
    Type:       Secret (a volume populated by a Secret)
    SecretName: default-token-q3u80
QoS Class:      Burstable
No events.
```
* 执行 `kubectl exec` 进入 container， 运行 `ll /dev/nvidia*`，查看GPU device，显示为两个设备 `/dev/nvidia0` 和 `/dev/nvidia1`
```
kubectl exec -it nvidia-gpu-test2 /bin/bash
root@nvidia-gpu-test2:/examples# ll /dev/nvidia*
crw-rw-rw-. 1 root root 245,   0 Sep 25 02:52 /dev/nvidia-uvm
crw-rw-rw-. 1 root root 195,   0 Sep 25 02:52 /dev/nvidia0
crw-rw-rw-. 1 root root 195,   1 Sep 25 02:52 /dev/nvidia1
crw-rw-rw-. 1 root root 195, 255 Sep 25 02:52 /dev/nvidiactl
```

## 测试二
与 测试一相比，增加验证在 pod 中实际使用 GPUs, 在 `gputest_volume.yaml` 中，添加了：
* 映射主机 GPU library (/var/lib/nvidia) 目录到 pod 中 /usr/local/nvidia/lib64
* 映射主机 Nvidia Tools 目录(/opt/bin) 到 pod 中 /usr/local/nvidia/bin ( 本步骤可选可选，为了执行 nvidia-smi 测试显示 GPU 信息 )
* 加入 `list_gpu.py` 测试调用 tensorflow 列出 GPU

测试步骤如下：
* 构建测试用 docker image
```
docker build -t list_gpu .
docker tag list_gpu 10.10.10.94:5000/liuqs/list_gpu
docker push 10.10.10.94:5000/liuqs/list_gpu
```


* 创建测试 pod
  ```
  kubectl create -f gputest_volume.yaml
  ```
* 查看 pod 信息
```
$ kubectl get po -o wide
NAME               READY     STATUS    RESTARTS   AGE       IP          NODE
test-list-gpu      1/1       Running   0          9m        10.1.72.2   10.10.10.94
```
pod 正常启动，并调度到 10.10.10.94 节点上，除了测试一的一些测试外，进行下面两项额外测试。

* 执行 `kubectl exec` 进入 container， 运行 `list_gpu.py`, 查看通过 tensorflow 列出的 GPU device
```
$ kubectl exec -it test-list-gpu /bin/bash
root@test-list-gpu:/examples# ls
list_gpu.py
root@test-list-gpu:/examples# python list_gpu.py
I tensorflow/stream_executor/dso_loader.cc:108] successfully opened CUDA library libcublas.so locally
I tensorflow/stream_executor/dso_loader.cc:108] successfully opened CUDA library libcudnn.so locally
I tensorflow/stream_executor/dso_loader.cc:108] successfully opened CUDA library libcufft.so locally
I tensorflow/stream_executor/dso_loader.cc:108] successfully opened CUDA library libcuda.so locally
I tensorflow/stream_executor/dso_loader.cc:108] successfully opened CUDA library libcurand.so locally
I tensorflow/core/common_runtime/gpu/gpu_init.cc:102] Found device 0 with properties:
name: GeForce GTX TITAN X
major: 5 minor: 2 memoryClockRate (GHz) 1.076
pciBusID 0000:04:00.0
Total memory: 11.92GiB
Free memory: 11.81GiB
W tensorflow/stream_executor/cuda/cuda_driver.cc:572] creating context when one is currently active; existing: 0x391bcf0
I tensorflow/core/common_runtime/gpu/gpu_init.cc:102] Found device 1 with properties:
name: GeForce GTX TITAN X
major: 5 minor: 2 memoryClockRate (GHz) 1.076
pciBusID 0000:05:00.0
Total memory: 11.92GiB
Free memory: 11.81GiB
I tensorflow/core/common_runtime/gpu/gpu_init.cc:126] DMA: 0 1
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 0:   Y Y
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 1:   Y Y
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce GTX TITAN X, pci bus id: 0000:04:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:806] Creating TensorFlow device (/gpu:1) -> (device: 1, name: GeForce GTX TITAN X, pci bus id: 0000:05:00.0)
[u'/gpu:0', u'/gpu:1']
```
* 执行 `kubectl exec` 进入 container， 运行 `nvidia-smi`，查看GPU信息
```
$ kubectl exec -it test-list-gpu /bin/bash
root@test-list-gpu:/examples# nvidia-smi
Sun Sep 25 08:23:12 2016
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 367.35                 Driver Version: 367.35                    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce GTX TIT...  Off  | 0000:04:00.0     Off |                  N/A |
| 22%   35C    P8    15W / 250W |      0MiB / 12206MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   1  GeForce GTX TIT...  Off  | 0000:05:00.0     Off |                  N/A |
| 22%   36C    P8    15W / 250W |      0MiB / 12206MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID  Type  Process name                               Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```

## References
* https://github.com/kubernetes/kubernetes/pull/28216
* https://github.com/kubernetes/kubernetes/pull/30756
* https://github.com/Hui-Zhi/kubernetes/blob/gpu-enhance-pr/docs/proposals/nvidia-gpu-enhancement.md
