# tf destribution


本例子可以在同一台机器跑 tf 分布式例子： 2 ps, 2 worker.

分别在4个不同的 terminal 运行下面的一条命令。

```bash
 python train.py \
     --ps_hosts=localhost:2222,localhost:2223 \
     --worker_hosts=localhost:2224,localhost:2225 \
     --job_name=ps --task_index=0
 python train.py \
     --ps_hosts=localhost:2222,localhost:2223 \
     --worker_hosts=localhost:2224,localhost:2225 \
     --job_name=ps --task_index=1
 python train.py \
     --ps_hosts=localhost:2222,localhost:2223 \
     --worker_hosts=localhost:2224,localhost:2225 \
     --job_name=worker --task_index=0
 python train.py \
     --ps_hosts=localhost:2222,localhost:2223 \
     --worker_hosts=localhost:2224,localhost:2225 \
     --job_name=worker --task_index=1
```


# logs

多个worker 之间有可能跑相同的 step, 注意下面两个 worker 的 logs.

worker 0
```txt

tep: 999901 weight: 2.00425195694 bias: 9.89888572693
=========> step: 999903 weight: 2.00425171852 bias: 9.89888572693
=========> step: 999905 weight: 2.00425291061 bias: 9.89888572693
=========> step: 999907 weight: 2.0042526722 bias: 9.89888572693
=========> step: 999909 weight: 2.00425243378 bias: 9.89888572693
=========> step: 999912 weight: 2.00425219536 bias: 9.89888572693
=========> step: 999914 weight: 2.00425195694 bias: 9.89888572693
=========> step: 999916 weight: 2.00425171852 bias: 9.89888572693
=========> step: 999918 weight: 2.0042514801 bias: 9.89888572693
=========> step: 999920 weight: 2.00425124168 bias: 9.89888572693
=========> step: 999922 weight: 2.00425100327 bias: 9.89888572693
=========> step: 999924 weight: 2.00425219536 bias: 9.89888572693
=========> step: 999927 weight: 2.00425195694 bias: 9.89888572693
=========> step: 999929 weight: 2.00425171852 bias: 9.89888572693
=========> step: 999931 weight: 2.0042514801 bias: 9.89888572693
=========> step: 999933 weight: 2.00425124168 bias: 9.89888572693
=========> step: 999935 weight: 2.00425100327 bias: 9.89888572693
=========> step: 999937 weight: 2.00425219536 bias: 9.89888572693
=========> step: 999939 weight: 2.00425195694 bias: 9.89888572693
=========> step: 999941 weight: 2.00425171852 bias: 9.89888572693
=========> step: 999944 weight: 2.0042514801 bias: 9.89888572693
=========> step: 999946 weight: 2.00425124168 bias: 9.89888572693
=========> step: 999948 weight: 2.00425100327 bias: 9.89888572693
=========> step: 999950 weight: 2.00425076485 bias: 9.89888572693
=========> step: 999952 weight: 2.00425052643 bias: 9.89888572693
=========> step: 999954 weight: 2.00425028801 bias: 9.89888572693
=========> step: 999957 weight: 2.0042514801 bias: 9.89888572693
=========> step: 999959 weight: 2.00425124168 bias: 9.89888572693
=========> step: 999961 weight: 2.00425100327 bias: 9.89888572693
=========> step: 999963 weight: 2.00425076485 bias: 9.89888572693
=========> step: 999965 weight: 2.00425052643 bias: 9.89888572693
=========> step: 999967 weight: 2.00425171852 bias: 9.89888572693
=========> step: 999970 weight: 2.0042514801 bias: 9.89888572693
=========> step: 999972 weight: 2.00425124168 bias: 9.89888572693
=========> step: 999974 weight: 2.00425100327 bias: 9.89888572693
=========> step: 999976 weight: 2.00425076485 bias: 9.89888572693
=========> step: 999979 weight: 2.00425195694 bias: 9.89888572693
=========> step: 999981 weight: 2.00425171852 bias: 9.89888572693
=========> step: 999983 weight: 2.0042514801 bias: 9.89888572693
=========> step: 999985 weight: 2.00425124168 bias: 9.89888572693
=========> step: 999987 weight: 2.00425100327 bias: 9.89888572693
=========> step: 999989 weight: 2.00425076485 bias: 9.89888572693
=========> step: 999991 weight: 2.00425195694 bias: 9.89888572693
=========> step: 999993 weight: 2.00425171852 bias: 9.89888572693
=========> step: 999996 weight: 2.0042514801 bias: 9.89888572693
=========> step: 999998 weight: 2.00425124168 bias: 9.89888572693
=========> step: 1000000 weight: 2.00425100327 bias: 9.89888572693
``

worker 1

```txt
=========> step: 999901 weight: 2.00425195694 bias: 9.89888572693
=========> step: 999903 weight: 2.00425171852 bias: 9.89888572693
=========> step: 999905 weight: 2.0042514801 bias: 9.89888572693
=========> step: 999907 weight: 2.00425124168 bias: 9.89888572693
=========> step: 999909 weight: 2.00425100327 bias: 9.89888572693
=========> step: 999911 weight: 2.00425076485 bias: 9.89888572693
=========> step: 999913 weight: 2.00425052643 bias: 9.89888572693
=========> step: 999915 weight: 2.00425028801 bias: 9.89888572693
=========> step: 999916 weight: 2.00425004959 bias: 9.89888572693
=========> step: 999918 weight: 2.0042514801 bias: 9.89888572693
=========> step: 999920 weight: 2.00425124168 bias: 9.89888572693
=========> step: 999922 weight: 2.00425100327 bias: 9.89888572693
=========> step: 999924 weight: 2.00425076485 bias: 9.89888572693
=========> step: 999926 weight: 2.00425052643 bias: 9.89888572693
=========> step: 999928 weight: 2.00425028801 bias: 9.89888572693
=========> step: 999930 weight: 2.00425004959 bias: 9.89888572693
=========> step: 999931 weight: 2.00424981117 bias: 9.89888572693
=========> step: 999933 weight: 2.00424957275 bias: 9.89888572693
=========> step: 999935 weight: 2.00425100327 bias: 9.89888572693
=========> step: 999937 weight: 2.00425076485 bias: 9.89888572693
=========> step: 999939 weight: 2.00425052643 bias: 9.89888572693
=========> step: 999941 weight: 2.00425028801 bias: 9.89888572693
=========> step: 999943 weight: 2.00425004959 bias: 9.89888572693
=========> step: 999945 weight: 2.00424981117 bias: 9.89888572693
=========> step: 999947 weight: 2.00424957275 bias: 9.89888572693
=========> step: 999949 weight: 2.00424933434 bias: 9.89888572693
=========> step: 999950 weight: 2.00424909592 bias: 9.89888572693
=========> step: 999952 weight: 2.00425052643 bias: 9.89888572693
=========> step: 999954 weight: 2.00425028801 bias: 9.89888572693
=========> step: 999956 weight: 2.00425004959 bias: 9.89888572693
=========> step: 999958 weight: 2.00424981117 bias: 9.89888572693
=========> step: 999960 weight: 2.00424957275 bias: 9.89888572693
=========> step: 999961 weight: 2.00425100327 bias: 9.89888572693
=========> step: 999963 weight: 2.00425076485 bias: 9.89888572693
=========> step: 999965 weight: 2.00425052643 bias: 9.89888572693
=========> step: 999967 weight: 2.00425028801 bias: 9.89888572693
=========> step: 999969 weight: 2.00425004959 bias: 9.89888572693
=========> step: 999971 weight: 2.00424981117 bias: 9.89888572693
=========> step: 999972 weight: 2.00424957275 bias: 9.89888572693
=========> step: 999974 weight: 2.00425100327 bias: 9.89888572693
=========> step: 999976 weight: 2.00425076485 bias: 9.89888572693
=========> step: 999978 weight: 2.00425052643 bias: 9.89888572693
=========> step: 999980 weight: 2.00425028801 bias: 9.89888572693
=========> step: 999982 weight: 2.00425004959 bias: 9.89888572693
=========> step: 999984 weight: 2.00424981117 bias: 9.89888572693
=========> step: 999985 weight: 2.00425124168 bias: 9.89888572693
=========> step: 999987 weight: 2.00425100327 bias: 9.89888572693
=========> step: 999989 weight: 2.00425076485 bias: 9.89888572693
=========> step: 999991 weight: 2.00425052643 bias: 9.89888572693
=========> step: 999993 weight: 2.00425028801 bias: 9.89888572693
=========> step: 999995 weight: 2.00425004959 bias: 9.89888572693
=========> step: 999997 weight: 2.00424981117 bias: 9.89888572693
=========> step: 999999 weight: 2.00424957275 bias: 9.89888572693
=========> step: 1000000 weight: 2.00424933434 bias: 9.89888572693
```

ps 0
```txt
[zhanghui@Megatron distributed-tf]$ python train.py \
>      --ps_hosts=localhost:2222,localhost:2223 \
>      --worker_hosts=localhost:2224,localhost:2225 \
>      --job_name=ps --task_index=0

2017-06-08 15:36:01.272814: I tensorflow/core/distributed_runtime/rpc/grpc_channel.cc:215] Initialize GrpcChannelCache for job ps -> {0 -> localhost:2222, 1 -> localhost:2223}
2017-06-08 15:36:01.272884: I tensorflow/core/distributed_runtime/rpc/grpc_channel.cc:215] Initialize GrpcChannelCache for job worker -> {0 -> localhost:2224, 1 -> localhost:2225}
2017-06-08 15:36:01.275430: I tensorflow/core/distributed_runtime/rpc/grpc_server_lib.cc:316] Started server with target: grpc://localhost:2222

```

ps 1
```txt
[zhanghui@Megatron distributed-tf]$ python train.py \
>      --ps_hosts=localhost:2222,localhost:2223 \
>      --worker_hosts=localhost:2224,localhost:2225 \
>      --job_name=ps --task_index=1

2017-06-08 15:36:39.443628: I tensorflow/core/distributed_runtime/rpc/grpc_channel.cc:215] Initialize GrpcChannelCache for job ps -> {0 -> localhost:2222, 1 -> localhost:2223}
2017-06-08 15:36:39.443698: I tensorflow/core/distributed_runtime/rpc/grpc_channel.cc:215] Initialize GrpcChannelCache for job worker -> {0 -> localhost:2224, 1 -> localhost:2225}
2017-06-08 15:36:40.212325: I tensorflow/core/distributed_runtime/rpc/grpc_server_lib.cc:316] Started server with target: grpc://localhost:2223
```
