import tensorflow as tf
import os
import json
from .engine import Engine
from .minho_package.data_process import *
from .minho_package.model import reRNN

PATH = os.path.dirname(os.path.realpath(__file__))


def init_model():
    sess = tf.Session()
    with open(os.path.join(PATH, 'minho_package/vocab.json'), 'r') as fp:
        vocab = json.load(fp)
    reverse_vocab = dict()
    for key, value in vocab.items():
        reverse_vocab[value] = key
    vocab_size = len(vocab)
    model = reRNN(sess=sess, name="reRNN", max_step=50, vocab_size=vocab_size)
    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint(PATH + "/minho_package/models"))

    return model, vocab, reverse_vocab

model, vocab, reverse_vocab = init_model()


class HosEngine(Engine):
    def activate(self, text):
        """
        반드시 오버라이딩 해야하는 메소드 입니다.
        APP은 이 메소드를 기준으로 엔진을 사용합니다.
        :param text: 한 글자
        :return: 모델링을 거친 문장
        """
        answer = self._model(text)

        return answer

    def _model(self, text):
        res = ""
        for t in text:
            number = find_vocab(t, vocab)
            if number == "retry":
                return ("[%s]로 시작하는 단어가 없습니다." % t)
            result = model.inference([number])
            r = reverse_vocab[number] + ' ' + indexToSentence(result, reverse_vocab)[0] + "\n"
            res += r

        return res[:-1]