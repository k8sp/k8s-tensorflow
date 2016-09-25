# Kubernetes with multi-GPUs
## Requirements:
* 集群 GPU 驱动已加载， GPU 工作正常
* Kubernetes 的主线版本（到目前为止为 v1.3.7）对 GPU 的调度支持不完善，本示例采用 https://github.com/kubernetes/kubernetes/pull/28216 提交的完善对 GPU 支持的 Kubernetes 版本（估计会在 v1.5.0 之后 merge 到 Kubernetes 主线版本），如何编译 Kubernetes 请参考 [build_k8s](../../build_k8s)。
* 使用编译后的 Kubernetes 集群工作正常。

## 测试一
* 构建测试用 docker image

  在 `gputest.yaml` 中使用的 docker image 是 `10.10.10.94:5000/mnist`, 构建参考[mnist](../mnist)
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

## 测试二
与 测试一相比，增加验证在 pod 中实际使用 GPUs, 在 `gputest_library.yaml` 中，添加了：
* 映射主机 GPU library (/var/lib/nvidia) 目录到 pod 中
* 映射主机 Nvidia Tools 目录(/opt/bin) 到 pod 中 /opt/bin/ (本步骤可选可选，为了执行 nvidia-smi 测试)

测试步骤如下：
* 构建测试用 docker image

  同测试一

* 创建测试 pod

  创建 pod：
  ```
  kubectl create -f gputest_library.yaml
  ```
* 查看 pod 信息
  ```
  ```
