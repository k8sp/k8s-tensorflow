#!/bin/


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
