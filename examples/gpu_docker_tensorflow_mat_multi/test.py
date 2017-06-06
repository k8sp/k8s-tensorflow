import tensorflow as tf

with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
  with tf.device('/cpu:0'):
    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2,3], name='a')
    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3,2], name='b')
    c = tf.matmul(a,b)
    print(sess.run(c))

with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
  with tf.device('/gpu:0'):
    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2,3], name='a')
    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3,2], name='b')
    c = tf.matmul(a,b)
    print(sess.run(c))

with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
    with tf.device('/cpu:0'):
	a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
	b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
    c = tf.matmul(a, b)
    print(sess.run(c))


with tf.Session(config=tf.ConfigProto(allow_soft_placement=True, log_device_placement=True)) as sess:
  with tf.device('/gpu:4'):
    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2,3], name='a')
    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3,2], name='b')
    c = tf.matmul(a,b)
    print(sess.run(c))

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
print(C)
print(sess.run(sum))

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


