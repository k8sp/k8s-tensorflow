#!/usr/bin/python

import tensorflow as tf
import numpy as np

# Flags for defining the tf.train.ClusterSpec
tf.app.flags.DEFINE_string("ps_hosts", "",
                           "Comma-separated list of hostname:port pairs")
tf.app.flags.DEFINE_string("worker_hosts", "",
                           "Comma-separated list of hostname:port pairs")

# Flags for defining the tf.train.Server
tf.app.flags.DEFINE_string("job_name", "", "One of 'ps', 'worker'")
tf.app.flags.DEFINE_integer("task_index", 0, "Index of task within the job")

FLAGS = tf.app.flags.FLAGS


def main(_):
  ps_hosts = FLAGS.ps_hosts.split(",")
  worker_hosts = FLAGS.worker_hosts.split(",")

  # Create a cluster from the parameter server and worker hosts.
  cluster = tf.train.ClusterSpec({"ps": ps_hosts, "worker": worker_hosts})

  # Create and start a server for the local task.
  server = tf.train.Server(cluster,
                           job_name=FLAGS.job_name,
                           task_index=FLAGS.task_index)

  if FLAGS.job_name == "ps":
    server.join()
  elif FLAGS.job_name == "worker":

    # Assigns ops to the local worker by default.
    train_X = np.linspace(-1,1,101)
    train_Y = 2 * train_X + np.random.randn(*train_X.shape) * 0.33 + 10

    X = tf.placeholder("float")
    Y = tf.placeholder("float")
    w = tf.Variable(0.0, name="weight")
    b = tf.Variable(0.0, name="reminder")

    init_op = tf.initialize_all_variables()
    cost_op = tf.square(Y - tf.multiply(X, w) - b)
    train_op = tf.train.GradientDescentOptimizer(0.01).minimize(cost_op)

    global_step = tf.Variable(0, trainable=False)

    with tf.device(tf.train.replica_device_setter(
        worker_device="/job:worker/task:%d" % FLAGS.task_index,
        cluster=cluster)):


      saver = tf.train.Saver()
      summary_op = tf.merge_all_summaries()
      init_op = tf.initialize_all_variables()

    # Create a "supervisor", which oversees the training process.
    sv = tf.train.Supervisor(is_chief=(FLAGS.task_index == 0),
                             logdir="/mnt/cephfs/test/train_logs",
                             init_op=init_op,
                             summary_op=summary_op,
                             saver=saver,
                             global_step=global_step,
                             save_model_secs=600)

    # The supervisor takes care of session initialization, restoring from
    # a checkpoint, and closing when done or an error occurs.
    with sv.managed_session(server.target) as sess:
      # Loop until the supervisor shuts down or 1000000 steps have completed.
      step = 0
      while not sv.should_stop() and step < 10:
        # Run a training step asynchronously.
        # See `tf.train.SyncReplicasOptimizer` for additional details on how to
        # perform *synchronous* training.

        train_feed = {X: train_X, Y: train_Y}
        _, step = sess.run([train_op, global_step], feed_dict= train_feed)
        print '=========> step: %d' % step
        print sess.run(w)
        print sess.run(b)

    # Ask for all the services to stop.
    sv.stop()

if __name__ == "__main__":
  tf.app.run()
