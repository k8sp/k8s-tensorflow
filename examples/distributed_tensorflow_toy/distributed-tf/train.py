import argparse
import sys

import tensorflow as tf
import numpy as np

FLAGS = None

def main(_):
	ps_hosts = FLAGS.ps_hosts.split(",")
 	worker_hosts = FLAGS.worker_hosts.split(",")
	
	# create a cluster from the parameter server and worker hosts
	cluster = tf.train.ClusterSpec({"ps": ps_hosts, "worker": worker_hosts})

	# create and start a server for the local task
        server = tf.train.Server(cluster,
				job_name=FLAGS.job_name,
				task_index=FLAGS.task_index)

	if FLAGS.job_name == "ps":
		server.join()
	elif FLAGS.job_name == "worker":
		# Assigns ops to the local worker by default.
		with tf.device(tf.train.replica_device_setter(
			worker_device="/job:worker/task:%d" % FLAGS.task_index,
			cluster=cluster)):
			
			#Build model
			train_X = np.linspace(-1.0, 1.0, 1000)
			train_Y = 2 * train_X + np.random.randn(*train_X.shape) * 0.33 + 10
			
			x = tf.placeholder("float")
			y = tf.placeholder("float")
			W = tf.Variable(0.0, name = 'weight')
			b = tf.Variable(0.0, name='bias')

			init_op = tf.global_variables_initializer()
			cost_op = tf.square(y - tf.multiply(x, W) - b)

			global_step = tf.contrib.framework.get_or_create_global_step()

			train_op = tf.train.AdagradOptimizer(0.01).minimize(cost_op, global_step=global_step)

			# the StopAtSetpHook handles stopping after running given steps.
			hooks=[tf.train.StopAtStepHook(last_step=10)]

			 # The MonitoredTrainingSession takes care of session initialization,
   			 # restoring from a checkpoint, saving to a checkpoint, and closing when done
 			 # or an error occurs.

			with tf.train.MonitoredTrainingSession(master=server.target,
								is_chief=(FLAGS.task_index == 0),
								checkpoint_dir='/tmp/train_logs',
								hooks=hooks) as mon_sess:
				while not mon_sess.should_stop():
					# Run a training step asynchronously.
				        # See `tf.train.SyncReplicasOptimizer` for additional details on how to
				        # perform *synchronous* training.
				        # mon_sess.run handles AbortedError in case of preempted PS.
					train_feed = {x: train_X, y: train_Y}
					_, step, weight, bias = mon_sess.run([train_op, global_step, W, b], feed_dict=train_feed)
					print('=========> step: {} weight: {} bias: {}'.format(step, weight, bias))


			print("end")

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.register("type", "bool", lambda v: v.lower() == 'true')

	# Flags for defining the tf.train.ClusterSpec
	parser.add_argument(
		"--ps_hosts",
		type=str,
		default="",
		help="Comma-separated list of hostname:port pairs"
	)
	parser.add_argument(
		"--worker_hosts",
		type=str,
		default="",
		help="Comma-separted list of hostname:port pairs"
	)
	parser.add_argument(
		"--job_name",
		type=str,
		default="",
		help="One of 'ps' , 'worker'"
	)

	# FLAGS	 for defining the tf.train.Server
	parser.add_argument(
		"--task_index",
		type=int,
		default=0,
		help='index of task within the job'
	)

	FLAGS, unparsed = parser.parse_known_args()
	tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)

	
