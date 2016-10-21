# k8s 使用 cephfs 创建 Persistent Volume

## 说明

实验目的：
- 验证在 k8s 使用 cephfs 创建 PersistentVolume
- 文档来源于对 https://github.com/k8sp/k8s-tensorflow/issues/5#issuecomment-240069845 的整理

实验基于:

- cepfs 配置: [https://github.com/kubernetes/kubernetes/tree/master/examples/volumes/cephfs](https://github.com/kubernetes/kubernetes/tree/master/examples/volumes/cephfs)
- Kernel 挂载方法: [https://github.com/k8sp/ceph/blob/master/mount-cephfs-on-linux-machine.md](https://github.com/k8sp/ceph/blob/master/mount-cephfs-on-linux-machine.md
)

下面是流程描述和注意事项

## 准备工作

正常运行的  ceph 集群:

- monitors: 10.10.10.191:6789, 10.10.10.93:6789, 10.10.10.94:6789
- ceph.admin.key: AQAlgLJXGCFfGxAAc5pcAlJ5QNteCSIsn35lqg==

## 创建 ceph 的 PersistentVolume 和  PersistentVolumeClaim

创建 ceph-pvc.yaml, 添加下面内容, 需要替换

- key: 使用 Base64 加密过的字符串(使用命令 `echo -n "AQAlgLJXGCFfGxAAc5pcAlJ5QNteCSIsn35lqg==" | base64`)
- monitors: 替换 ceph 集群中的 monitors 信息
- path: 设置挂载 cephfs 中的 /exports 目录为根(ceph 中 /exports 需要提前创建)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ceph-secret
data:
  key: QVFBbGdMSlhHQ0ZmR3hBQWM1cGNBbEo1UU50ZUNTSXNuMzVscWc9PQ==
---
kind: PersistentVolume
apiVersion: v1
metadata:
  name: tf-ceph
  namespace: default
spec:
    capacity:
        storage: 100Gi
    accessModes:
        - ReadWriteMany
    cephfs:
      monitors:
      - 10.10.10.93:6789
      - 10.10.10.94:6789
      - 10.10.10.191:6789
      user: admin
      path: /exports
      secretRef:
        name: ceph-secret
      readOnly: false
---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: tf-ceph
  namespace: default
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 100Gi
```

开始创建名为 tf-ceph 的 PersistentVolume 和 PersistentVolumeClaim

```bash
# 创建 ceph-pvc
kubectl create -f ceph-pvc.yaml
# 查看持久卷状态
kubectl get pv,pvc
```

### 使用持久卷

创建 load_data.yaml 文件

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: load-data
spec:
  template:
    metadata:
      name: load-data
    spec:
      restartPolicy: Never
      containers:
        - name: loader
          image: 10.10.10.94:5000/liuqs/tensorflow:0.10.0-gpu
          command:
              - "/bin/sh"
              - "-c"
          args:
            - "curl https://storage.googleapis.com/oscon-tf-workshop-materials/processed_reddit_data/news_aww/prepared_data.tar.gz | tar xzv -C /var/tensorflow/"
          volumeMounts:
            - name: tf-ceph
              mountPath: /var/tensorflow
      volumes:
        - name: tf-ceph
          persistentVolumeClaim:
            claimName: tf-ceph
```

执行 load_data.yaml 任务

```bash
kubectl create -f load_data.yaml
# 查看任务状态, 是否有报错, 直到正常运行
kubectl describe pod load-data
```

通过上面的流程跑通了使用 cephfs 创建 PersistentVolume 和 PersistentVolumeClaim, 并能正确导入数据, 完成了 ceph 和 k8s 结合. tensorflow 或其他的 pod 只需要加入下面配置块, 就能正常挂载 ceph 了.
- mountPath: 挂载到容器中的路径
```yaml
kind: Pod
apiVersion: v1
metadata:
  name: mypod
spec:
  containers:
    - name: test_ceph_volume
      image: 10.10.10.94:5000/liuqs/tensorflow:0.10.0-gpu
      volumeMounts:
      - mountPath: "/var/tensorflow"
        name:  tf-ceph
  volumes:
    - name:  tf-ceph
      persistentVolumeClaim:
        claimName:  tf-ceph
```

## 注意事项
http://kubernetes.io/docs/user-guide/persistent-volumes/

`
Important! A volume can only be mounted using one access mode at a time, even if it supports many. For example, a GCEPersistentDisk can be mounted as ReadWriteOnce by a single node or ReadOnlyMany by many nodes, but not at the same time.
`

## References:
* http://kubernetes.io/docs/user-guide/persistent-volumes/
