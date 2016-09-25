# Run CPU distributed tensorflow on k8s

实验目标：
- 在 k8s 上运行 CPU version distributed tensorflow

实验基于：
- 实验基于对 https://github.com/k8sp/k8s-tensorflow/issues/5#issue-170827254 整理
-  [https://github.com/amygdala/tensorflow-workshop/tree/master/workshop_sections/distributed_tensorflow](https://github.com/amygdala/tensorflow-workshop/tree/master/workshop_sections/distributed_tensorflow)

下面会记录实验流程和注意事项.

## 准备工作

- kubectl 能够正确连接 k8s 集群
- Clone 这个仓库([amygdala](https://github.com/amygdala)/**tensorflow-workshop**) 到本地

## 创建 Ceph Persistent Volume

参照在 k8s 中使用 ceph Persistent Volume



## 创建 Tensorboard Server

```bash
kubectl create -f k8s-configs/tensorboard.yaml
# 可以通过集群中任意 Node IP 加下面 NodePort 登录到 WEBUI(如: 10.10.10.203:31175)
kubectl describe services tensorboard
Name:			tensorboard
Namespace:		default
Labels:			<none>
Selector:		tensorflow=tensorboard
Type:			LoadBalancer
IP:			10.3.0.92
Port:			<unset>	80/TCP
NodePort:		<unset>	31175/TCP
Endpoints:		10.1.62.2:6006
Session Affinity:	None
No events.
```

## 启动 Tensorflow Job

任务会拉取 `gcr.io/google-samples/tf-worker-example:latest` 这个镜像(740MB), 每个 Node 都会拉取, 速度很慢会导致任务失败.

这边解决方法是上传到 163 的 docker hub 上, 得到 `hub.c.163.com/vienlee/tf-worker-example:latest` , 替换 [tf-cluster.yaml](https://github.com/amygdala/tensorflow-workshop/blob/master/workshop_sections/distributed_tensorflow/k8s-configs/tf-cluster.yaml) 中的 `gcr.io/google-samples/tf-worker-example:latest` 地址为`hub.c.163.com/vienlee/tf-worker-example:latest` 即可.

之所以没有用私有仓库, 因为当前没有搭建可用的私有仓库, 而且还需要支持 https(否则需要修改每个 Node 的 docker 配置增加私有仓库地址)

```bash
kubectl create -f tf-cluster.yaml
# 查看每个 pod 的状态
kubectl get pod
# 查看 pod 创建日志是否正常
kubectl describe pod <podname>
```

等待所有 Pod 创建成功, 状态为 Runing.

## 总结
通过实验证明 tensorflow 可以正常在 k8s 上运行, 后续流程我们可以提前创建 pv(使用 cephfs 存储) 和 pvc, 把训练数据导入到 pv 中. 然后编译我们自己的任务镜像, 编排 tf-cluster.yaml 执行任务.  
