# A Tutorial: Tensorflow on Kubernetes(multi GPUs on single node)

本Tutorial记录如何在kubernetes上运行一个多机单gpu的tensorflow seq2seq模型

## 摘要
1. pull tensorflow images from dockerhub
2. push tensorflow images to harbor
3. 创建、编辑yaml

   1) 创建一个ps service(对应一个ps pod)

   2) 创建两个worker service(分别对应一个worker pod)

   注意：因为ps和worker节点需要对外暴露自己位置(域名)，所以需要每个pod(container)对应一个service，并配合kube-dns进行服务发现，参考下面一个官方例子和一个民间例子
   https://github.com/tensorflow/ecosystem/blob/master/kubernetes/template.yaml.jinja
   https://github.com/amygdala/tensorflow-workshop/blob/9bbc678e686407c5dccff87db702f9aeef9e34b7/workshop_sections/distributed_tensorflow/k8s-configs/tf-cluster.yaml

4. 获取tensorflow训练代码和数据

   pod挂在nfs，代码和数据存放在nfs服务端内

   数据地址:
   translate.py中有下载数据的流程、也可以单独下载解压到./dir/data中
```python
   _WMT_ENFR_TRAIN_URL = "http://www.statmt.org/wmt10/training-giga-fren.tar"
   _WMT_ENFR_DEV_URL = "http://www.statmt.org/wmt15/dev-v2.tgz"
```

## Requirements:
1. 正常运行的k8s集群
2. k8s集群支持gpu，alpha.kubernetes.io/nvidia-gpu字段可以正常使用

## Step 1: Prepare Tensorflow Images:
```shell
[xuerq@bogon train]$ docker pull tensorflow/tensorflow:0.10.0-devel-gpu
064f9af02539: Already exists 
390957b2f4f0: Already exists 
cee0974db2b8: Already exists 
ff4090f99abc: Pull complete 
70d51ddf7c95: Pull complete 
da76ab5d6dff: Pull complete 
46d4527e85d3: Pull complete 
528276ea4b2d: Pull complete 
709fc41158c6: Pull complete 
d63463802d36: Pull complete 
b4c3589c6b3a: Pull complete 
Digest: sha256:0635a564b59ac45e9a44d7c38efee9bf6c9567150236e064d8e382fbbf54fe74
Status: Downloaded newer image for tensorflow/tensorflow:0.10.0-devel-gpu
```
login harbor:
由于kubernete集群访问外网不是很方便，速度也无法保证。所以我们首先需要将镜像推送至私有仓库，方便日常使用
```shell
docker login https://harbor.ail.unisound.com
Username: xueruiqing
Password: 
Login Succeeded
```
登陆节点配置证书(如需要):
参考https://github.com/k8sp/k8s-tensorflow/tree/master/harbor
```shell
sudo bash ./update_certs_centos.sh harbor.ail.unisound.com ca.crt
```

tag & push image to harbor:
```shell
[xuerq@bogon train]$ docker tag ef9825a3a86f harbor.ail.unisound.com/xuerq/tensorflow:0.10.0-devel-gpu
[xuerq@bogon train]$ docker push harbor.ail.unisound.com/xuerq/tensorflow:0.10.0-devel-gpu
```

## Step 2: create ps & worker:
1. 创建1个ps节点、2个worker节点
2. 2个worker节点共用一份训练数据，存放在挂在的nfs目录中;log和模型输出也分别在nfs的单独的目录中
3. 通过nvidia-libs-volume挂在宿主机/usr/local/nvidia/lib64, cuda库等
4. 通过nvidia-tools-volume挂在宿主机/usr/bin，nvidia-smi等 
5. 通过alpha.kubernetes.io/nvidia-gpu:1,申请宿主机gpu配额

```shell
[xuerq@bogon train]$ kubectl create -f worker_ps_service_GPU.yaml
```
```yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    name: tensorflow-ps
    role: service
  name: tensorflow-ps-service
spec:
  ports:
    - port: 2222
      targetPort: 2222
  selector:
    name: tensorflow-ps
---
apiVersion: v1
kind: Service
metadata:
  labels:
    name: tensorflow-worker0
    role: service
  name: tensorflow-wk-service0
spec:
  ports:
    - port: 2222
      targetPort: 2222
  selector:
    name: tensorflow-worker0
---
apiVersion: v1
kind: Service
metadata:
  labels:
    name: tensorflow-worker1
    role: service
  name: tensorflow-wk-service1
spec:
  ports:
    - port: 2222
      targetPort: 2222
  selector:
    name: tensorflow-worker1

```

```shell
[xuerq@bogon train]$ kubectl describe service #得到 ps 和 worker service 的 ip 和端口
```
```shell
Name:			tensorflow-ps-service
Namespace:		default
Labels:			name=tensorflow-ps
			role=service
Selector:		name=tensorflow-ps
Type:			ClusterIP
IP:			10.100.0.153
Port:			<unset>	2222/TCP
Endpoints:		<none>
Session Affinity:	None
No events.

Name:			tensorflow-wk-service0
Namespace:		default
Labels:			name=tensorflow-worker0
			role=service
Selector:		name=tensorflow-worker0
Type:			ClusterIP
IP:			10.100.0.174
Port:			<unset>	2222/TCP
Endpoints:		<none>
Session Affinity:	None
No events.

Name:			tensorflow-wk-service1
Namespace:		default
Labels:			name=tensorflow-worker1
			role=service
Selector:		name=tensorflow-worker1
Type:			ClusterIP
IP:			10.100.0.119
Port:			<unset>	2222/TCP
Endpoints:		<none>
Session Affinity:	None
No events.
```



```shell
[xuerq@bogon train]$ kubectl create -f worker_ps_GPU.yaml #此处需要填入 ps 和 worker 的ip 和端口
```
**worker_ps_rc_GPU.yaml**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: tensorflow-cluster-config
data:
  ps: 
     "10.100.0.153:2222"
  worker:
     "10.100.0.174:2222,\
      10.100.0.119:2222"
---
apiVersion: batch/v1
kind: Job
metadata:
  name: tensorflow-ps-rc
spec:

  template:
    metadata:
      labels:
        name: tensorflow-ps
        role: ps
    spec:
      containers:
      - name: ps
        image: harbor.ail.unisound.com/xuerq/tensorflow:0.10.0-devel-gpu
        ports:
        - containerPort: 2222
        env:
        - name: PS_KEY
          valueFrom:
            configMapKeyRef:
              name: tensorflow-cluster-config
              key: ps
        - name: WORKER_KEY
          valueFrom:
            configMapKeyRef:
              name: tensorflow-cluster-config
              key: worker
        command: ["/bin/sh", "-c"]
        args: ["cd /root/tensorflow; \
                rm -rf ./train_ps; \
                mkdir ./train_ps; \
                python translate.py \
                   --job_name=ps \
                   --task_index=0 \
                   --ps_hosts=$(PS_KEY) \
                   --worker_hosts=$(WORKER_KEY) \
                   --num_layers=2  --size=200 \
                   --data_dir=./data  --train_dir=./train_ps \
                   1>./train_ps/log \
                   2>./train_ps/errlog
               "]
        volumeMounts:
        - name: work-path
          mountPath: /root/tensorflow
          readOnly: false
      restartPolicy: Never
      volumes:
      - name: work-path
        hostPath: 
          path: /root/tensorflow
      nodeName: 0c-c4-7a-82-c5-bc
---
apiVersion: batch/v1
kind: Job
metadata:
  name: tensorflow-worker0-rc
spec:
  template:
    metadata:
      labels:
        name: tensorflow-worker0
        role: worker
    spec:
      containers:
      - name: worker
        image: harbor.ail.unisound.com/xuerq/tensorflow:0.10.0-devel-gpu
        resources:
          limits:
            alpha.kubernetes.io/nvidia-gpu: 1
        ports:
        - containerPort: 2222
        env:
        - name: PS_KEY
          valueFrom:
            configMapKeyRef:
              name: tensorflow-cluster-config
              key: ps
        - name: WORKER_KEY
          valueFrom:
            configMapKeyRef:
              name: tensorflow-cluster-config
              key: worker
        command: ["/bin/sh", "-c"]
        args: ["cd /root/tensorflow; \
                rm -rf ./train_worker0; \
                mkdir ./train_worker0; \
                export CUDA_VISIBLE_DEVICES=0; \
                python translate.py \
                   --job_name=worker \
                   --task_index=0 \
                   --ps_hosts=$(PS_KEY) \
                   --worker_hosts=$(WORKER_KEY) \
                   --num_layers=2  --size=200 \
                   --data_dir=./data  --train_dir=./train_worker0 \
                   1>./train_worker0/log \
                   2>./train_worker0/errlog
               "]
        volumeMounts:
        - name: work-path
          mountPath: /root/tensorflow
          readOnly: false
        - name: nvidia-libs-volume
          mountPath: /usr/local/nvidia/lib64
          readOnly: true
        - name: nvidia-tools-volume
          mountPath: /usr/local/nvidia/bin
          readOnly: true
      restartPolicy: Never
      volumes:
      - name: work-path
        hostPath: 
          path: /root/tensorflow
      - name: nvidia-libs-volume
        hostPath: 
          path: /usr/local/nvidia/lib64
      - name: nvidia-tools-volume
        hostPath: 
          path: /usr/bin
      nodeName: 0c-c4-7a-82-c5-bc
---
apiVersion: batch/v1
kind: Job
metadata:
  name: tensorflow-worker1-rc
spec:
  template:
    metadata:
      labels:
        name: tensorflow-worker1
        role: worker
    spec:
      containers:
      - name: worker
        image: harbor.ail.unisound.com/xuerq/tensorflow:0.10.0-devel-gpu
        resources:
          limits:
            alpha.kubernetes.io/nvidia-gpu: 1
        ports:
        - containerPort: 2222
        env:
        - name: PS_KEY
          valueFrom:
            configMapKeyRef:
              name: tensorflow-cluster-config
              key: ps
        - name: WORKER_KEY
          valueFrom:
            configMapKeyRef:
              name: tensorflow-cluster-config
              key: worker
        command: ["/bin/sh", "-c"]
        args: ["cd /root/tensorflow; \
                rm -rf ./train_worker1; \
                mkdir ./train_worker1; \
                export CUDA_VISIBLE_DEVICES=0; \
                python translate.py \
                   --job_name=worker \
                   --task_index=1 \
                   --ps_hosts=$(PS_KEY) \
                   --worker_hosts=$(WORKER_KEY) \
                   --num_layers=2  --size=200 \
                   --data_dir=./data  --train_dir=./train_worker1 \
                   1>./train_worker1/log \
                   2>./train_worker1/errlog
               "]
        volumeMounts:
        - name: work-path
          mountPath: /root/tensorflow
          readOnly: false
        - name: nvidia-libs-volume
          mountPath: /usr/local/nvidia/lib64
          readOnly: true
        - name: nvidia-tools-volume
          mountPath: /usr/local/nvidia/bin
          readOnly: true
      restartPolicy: Never
      volumes:
      - name: work-path
        hostPath: 
          path: /root/tensorflow
      - name: nvidia-libs-volume
        hostPath: 
          path: /usr/local/nvidia/lib64
      - name: nvidia-tools-volume
        hostPath: 
          path: /usr/bin
      nodeName: 0c-c4-7a-82-c5-bc

```
## To be continued
## References
* http://www.cnblogs.com/xuxinkun/p/5983633.html
* http://kubernetes.io/docs/user-guide/getting-into-containers/

