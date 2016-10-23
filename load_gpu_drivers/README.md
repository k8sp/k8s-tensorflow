# Setup GPU on CoreOS

## 准备驱动

将[编译 GPU 驱动]((../build_gpu_drivers))生成的三个压缩包复制到 `setup_gpu.sh` 同目录

压缩包 | 说明
-------|-------
libraries-[DRIVER_VERSION].tar.bz2 | GPU 动态库
tools-[DRIVER_VERSION].tar.bz2 | GPU 工具
modules-[COREOS_VERSION]-[DRIVER_VERSION].tar.bz2 | GPU 驱动


## 加载驱动

以 `DRIVER_VERSION=367.57` 和 `COREOS_VERSION=1122.2.0` 为例：
执行如下命令完成 GPU 配置：
```bash
sudo bash ./setup_gpu.sh 1122.2.0 367.57
```

## 测试
**查看 GPU 信息**

```
# nvidia-smi
```
```
# docker run -it --rm --privileged cuda /bin/bash
# root@9a1ab2d177b0:/opt/nvidia# ./nvidia-smi
```
