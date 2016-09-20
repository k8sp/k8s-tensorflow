# Nvidia GPU drivers on CoreOS

## 编译方法对比
编译方法：
* 方法 A：https://github.com/emergingstack/es-dev-stack
* 方法 B：https://github.com/Clarifai/coreos-nvidia 此方法编译方便，推荐

方案  | CoreOS Version | Nvidia driver 352.39 | Nvidia driver 367.35
--------|----------------|----|----
方法 A | 1010.5.0(4.5.0-coreos-rc1)  | 工作正常 | 编译通过，不能正常工作（undefined in Nvidia-uvm）
方法 A | 1068.9.0(4.6.3-coreos)   | 编译不通过 https://github.com/k8sp/k8s-tensorflow/issues/12 | 未尝试
方法 B | 1010.5.0(4.5.0-coreos-rc1)   | 需要修改，打补丁 nvprocfs.patch | 编译通过，不能正常工作（undefined in Nvidia-uvm）
方法 B | 1068.9.0(4.6.3-coreos)   | 编译不通过 https://github.com/k8sp/k8s-tensorflow/issues/12  | 工作正常

注：
* 方法 B 是在CentOS 7.2.1511 测试， systemd-nspawn 版本为 219，比 https://github.com/Clarifai/coreos-nvidia  建议的版本 229 低
* 方法 B 只给出了编译 Nvidia driver，后续操作需参考方法 A
* 方法 B 简单方便，优于方法 A，推荐

**结论：**

**采用 方法B 编译 + 1068.9.0(4.6.3-coreos) + Nvidia driver 367.35**

**运行应用程序只需加载已编译好的驱动，不需要再重新编译**

## Compile GPU drivers (方法B)
编译不需要在 CoreOS 系统上，以 CentOS 7.2.1511 为例， systemd-nspawn 版本为 219。

<tt><a href="build.sh">build.sh</a> DRIVER_VERSION CHANNEL COREOS_VERSION</tt>

e.g.

`./build.sh 367.35 stable 1068.9.0`

The scripts will download both the official NVIDIA archive and the CoreOS
developer images, caching them afterwards. It will then create three archives:

```
libraries-[DRIVER_VERSION].tar.bz2
tools-[DRIVER_VERSION].tar.bz2
modules-[COREOS_VERSION]-[DRIVER_VERSION].tar.bz2
```

说明：
1.


## 加载 drivers

参照：[load GPU drivers](../load_gpu_drivers)


## 测试
**查看 GPU 信息**

```
# docker run -it --rm --privileged cuda /bin/bash
# root@9a1ab2d177b0:/opt/nvidia# ./nvidia-smi
```

## 参考
* 方法 A：https://github.com/emergingstack/es-dev-stack
* 方法 B：https://github.com/Clarifai/coreos-nvidia
* http://www.emergingstack.com/2016/01/10/Nvidia-GPU-plus-CoreOS-plus-Docker-plus-TensorFlow.html
* http://tleyden.github.io/blog/2014/11/04/coreos-with-nvidia-cuda-gpu-drivers/
* https://github.com/indigo-dc/Ubuntu1404_pyopencl/blob/master/Dockerfile
* https://github.com/NVIDIA/nvidia-docker/wiki/CUDA#requirements
