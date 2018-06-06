import tensorflow as tf

from .engine import Engine
from .minho_package.data_process import *
from .minho_package.model import reRNN

def init_model():
    sess = tf.Session()
    data = read_txt('novel.txt')
    data = preprocess(data)
    vocab, reverse_vocab, vocab_size = build_vocab(data)
    model = reRNN(sess=sess, name="reRNN", max_step=50, vocab_size=vocab_size)
    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint(PATH + "/models"))

    return model, vocab

model, vocab = init_model()
reverse_vocab = inv_map = {v: k for k, v in vocab.items()}


class HosEngine(Engine):
    def activate(self, text):
        """
        반드시 오버라이딩 해야하는 메소드 입니다.
        APP은 이 메소드를 기준으로 엔진을 사용합니다.
        :param text: 한 글자
        :return: 모델링을 거친 문장
        """
        answer = self.model(text)

        return answer

    def model(self, text):
        res = ""
        for t in text:
            number = find_vocab(t, vocab)
            if number == "retry":
                return "Fail"
            result = model.inference([number])
            r = reverse_vocab[number] + ' ' + indexToSentence(result, reverse_vocab)[0] + "\n"
            res += r

        return res