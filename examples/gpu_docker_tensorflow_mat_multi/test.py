import tensorflow as tf

print("matrix matmul in cpu")
with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
  with tf.device('/cpu:0'):
    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2,3], name='a')
    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3,2], name='b')
    c = tf.matmul(a,b)
    print(sess.run(c))

print("matrix matmul in gpu with 70% gpu memrory")
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.7)
with tf.Session(config=tf.ConfigProto(log_device_placement=True, gpu_options=gpu_options)) as sess:
  with tf.device('/gpu:0'):
    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2,3], name='a')
    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3,2], name='b')
    c = tf.matmul(a,b)
    print(sess.run(c))


print("matrix matmul in gpu that not exit, but use allow_soft_placement flag")
print()
with tf.Session(config=tf.ConfigProto(allow_soft_placement=True, log_device_placement=True)) as sess:
  with tf.device('/gpu:4'):
    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2,3], name='a')
    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3,2], name='b')
    c = tf.matmul(a,b)
    print(sess.run(c))

print("Matrix matmul with tower gpus")
# multi-gpu
c = []
for d in ['/gpu:0', '/gpu:1', '/gpu:2']:
	with tf.device(d):
	    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2,3], name='a')
	    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3,2], name='b')
	    c.append(tf.matmul(a,b))

with tf.device('/cpu:0'):
    sum = tf.add_n(c)

sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
print(c)
print(sess.run(sum))

print("matrix matmul in gpu that not exit, with catch tf.erros.InvalidArgumentError exception ")
# must exception
try:
	with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
	  with tf.device('/gpu:4'):
	    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2,3], name='a')
	    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3,2], name='b')
	    c = tf.matmul(a,b)
	    print(sess.run(c))
except tf.errors.InvalidArgumentError as e:
	print(e)


