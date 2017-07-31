import time
import numpy as np
import threading

import tensorflow as tf
from tensorflow.python.client import timeline


def test_queue():

    feature_input = tf.placeholder(tf.float32, shape=[None, 30, 49, 512], name="queue_inputs")
    target_intput = tf.placeholder(tf.float32, shape=[None, 30], name="queue_targets")

    queue = tf.FIFOQueue(
        capacity=1000,
        dtypes=[tf.float32, tf.float32],
        shapes=[[30, 49, 512], [30]],
        name="FIFOQueue"
    )

    # Enqueue and dequeue operations
    enqueue_op = queue.enqueue_many([feature_input, target_intput])
    queue_inputs, queue_targets = queue.dequeue_many(64)

    queue_size = queue.size()

    # Very simple training operator, dequeue examples from the FIFOQueue and
    # square the matrix elementwise. Just for testing of course.
    square_op = tf.square(queue_inputs)

    # Coordinator for threads
    coord = tf.train.Coordinator()

    # Initialize the TensorFlow session
    gpu_options = tf.GPUOptions(
        per_process_gpu_memory_fraction=0.75,
    )

    sess = tf.Session(config=tf.ConfigProto(
        gpu_options=gpu_options,
        log_device_placement=False,
        allow_soft_placement=False
    ))

    def load_and_enqueue():
        while True:
            # Just feed random stuff to the queue
            #features = np.random.rand(64, 30, 49, 512)
            features = np.ones([64, 30, 49, 512], dtype=np.float32)
            targets  = np.ones([64, 30], dtype=np.float32)

            # Feed example to Tensorflow placeholder
            feed_dict = {
                feature_input: features,
                target_intput: targets
            }

            # Push all the training examples to the queue
            # queue is not need to tf.initialize_all_variables()
            sess.run(enqueue_op, feed_dict=feed_dict)

            if coord.should_stop():
                break

    # Start the threads
    num_threads = 4
    for i in range(num_threads):
        t = threading.Thread(target=load_and_enqueue)
        t.setDaemon(True)
        t.start()

    # Make sure the queue is filled with some examples (n = 500)
    num_samples_in_queue = 0
    while num_samples_in_queue < 500:
        num_samples_in_queue = sess.run(queue_size)
        print("Initializing queue, current size = %i" % num_samples_in_queue)
        time.sleep(1)

    # Initialize the session
    init = tf.initialize_all_variables()
    sess.run(init)

    # for timeline of dequeue  benchmark 
    run_options  = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
    run_metadata = tf.RunMetadata()

    for step in range(1000):

        print("Step = %i, QueueSize = %i" % (step, sess.run(queue_size)))

        if step == 10:
            # Perform a step with saving the results as timeline object
            result = sess.run(square_op, options=run_options, run_metadata=run_metadata)

            # Create the Timeline object, and write it to a json
            tl = timeline.Timeline(run_metadata.step_stats)
            ctf = tl.generate_chrome_trace_format()
            with open('timeline.json', 'w') as f:
                print("writing to timeline.json")
                f.write(ctf)

        else:
            # Perform a step without saving the results
            result = sess.run(square_op)

    # Ask for the threads to stop
    coord.request_stop()
    sess.close()


if __name__ == "__main__":
    test_queue()
