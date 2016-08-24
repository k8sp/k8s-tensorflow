#! /bin/bash

# 进入脚本所在目录
cd `dirname $0`

# 创建目录
mkdir -p /opt/bin
mkdir -p /var/lib/nvidia

# 创建配置文件
TEMPLATE=/etc/ld.so.conf.d/nvidia.conf
[ -f $TEMPLATE ] || {
    echo "TEMPLATE: $TEMPLATE"
    mkdir -p $(dirname $TEMPLATE)
    cat << EOF > $TEMPLATE
/var/lib/nvidia
EOF
}

# 加载驱动
insmod modules/nvidia.ko
insmod modules/nvidia-uvm.ko

# 复制 tools 到 /opt/bin
cp tools/* /opt/bin

# 复制 libraries 到 /var/lib/nvidia
cp libraries/* /var/lib/nvidia/

# 刷新 lib 文件
ldconfig

# 执行 mkdevs
./mkdevs.sh
