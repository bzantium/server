import tensorflow as tf
from .model import reRNN
from .data_process import *
import os

if __name__ == "__main__":
    PATH = 'models'
    sess = tf.Session()
    data = read_txt('novel.txt')
    data = preprocess(data)
    vocab, reverse_vocab, vocab_size = build_vocab(data)
    model = reRNN(sess=sess, name="reRNN", max_step=20, vocab_size=vocab_size)
    sess.run(tf.global_variables_initializer())
    batches = batch_iter(data, batch_size=64, num_epochs=1000)
    saver = tf.train.Saver()
    avgLoss = []
    for step, batch in enumerate(batches):
        x_train, y_train = sentenceToIndex(batch, vocab)
        l, _ = model.train(x_train, y_train)
        avgLoss.append(l)
        if step % 500 == 0:
            print('batch:', '%04d' % step, 'loss:', '%05f' % np.mean(avgLoss))
            saver.save(sess, os.path.join(PATH, 'my-model.ckpt'), global_step=step)
            avgLoss = []