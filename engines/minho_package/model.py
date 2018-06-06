import tensorflow as tf

class reRNN:
    def __init__(self, sess, name, max_step, vocab_size):
        self.sess = sess
        self.name = name
        self.max_step = max_step
        self.vocab_size = vocab_size
        self._build_net()

    def _build_net(self):
        hidden_size = 128
        embedding_size = 300
        with tf.name_scope(self.name):
            self.first_input = tf.placeholder(tf.int32, shape=(None, ))
            self.full_input = tf.placeholder(tf.int32, shape=(None, None))
            input_length = tf.reduce_sum(tf.sign(self.full_input), axis=1)
            self.target = tf.placeholder(tf.int32, shape=(None, None))
            target_length = tf.reduce_sum(tf.sign(self.target), axis=1) + 1
            self.embedding = tf.Variable(tf.random_uniform(shape=[self.vocab_size, embedding_size], minval=-1.0, maxval=1.0))
            self.cell = tf.nn.rnn_cell.BasicLSTMCell(hidden_size)
            self.W = tf.Variable(tf.truncated_normal(shape=(hidden_size, self.vocab_size)))
            self.b = tf.Variable(tf.constant(0.1, shape=(self.vocab_size, )))
            batch_size, max_time_step = tf.unstack(tf.shape(self.full_input))
            embedded_full_input = tf.nn.embedding_lookup(self.embedding, self.full_input)
            outputs, _ = tf.nn.dynamic_rnn(self.cell,
                                           embedded_full_input,
                                           input_length,
                                           dtype=tf.float32) # outputs: [batch, time, hidden], bw_outputs: [batch, time, hidden]
            outputs = tf.reshape(outputs, [-1, hidden_size]) # output: [batch*time, hidden]
            logits = tf.add(tf.matmul(outputs, self.W), self.b) # logits: [batch*time, vocab_size]
            logits = tf.reshape(logits, [batch_size, max_time_step, -1]) # logits: [batch, time, vocab_size]
            self.loss = tf.reduce_mean(tf.contrib.seq2seq.sequence_loss(logits=logits,
                                                                        targets=self.target,
                                                                        weights=tf.sequence_mask(target_length, max_time_step,
                                                                        dtype=tf.float32)))

            global_step = tf.Variable(0, trainable=False)
            starter_learning_rate = 0.1
            learning_rate = tf.train.exponential_decay(starter_learning_rate, global_step,
                                                       1e+3, 0.96, staircase=True)
            optimizer = tf.train.AdamOptimizer(learning_rate)
            #self.train_op = optimizer.minimize(self.loss)
            gvs = optimizer.compute_gradients(self.loss)
            capped_gvs = [(tf.clip_by_value(grad, -1., 1.), var) for grad, var in gvs]
            self.train_op = optimizer.apply_gradients(capped_gvs, global_step=global_step)

            batch_size = tf.unstack(tf.shape(self.first_input))[0]
            state = self.cell.zero_state(batch_size, dtype=tf.float32)
            self.predictions = []
            prediction = 0
            for i in range(self.max_step):
                if i==0:
                    input_ = tf.nn.embedding_lookup(self.embedding, self.first_input)
                else:
                    input_ = tf.nn.embedding_lookup(self.embedding, prediction)
                output, state = self.cell(input_, state)
                inf_logits = tf.add(tf.matmul(output, self.W), self.b)
                prediction = tf.argmax(inf_logits, 1)
                self.predictions.append(prediction)
            self.predictions = tf.stack(self.predictions, 1)

    def setMaxStep(self, max_step):
        self.max_step = max_step

    def train(self, full_input, target):
        return self.sess.run([self.loss, self.train_op], feed_dict={self.full_input: full_input, self.target: target})

    def inference(self, first_input):
        return self.sess.run(self.predictions, feed_dict={self.first_input: first_input})