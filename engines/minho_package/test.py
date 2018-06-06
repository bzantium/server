from .data_process import read_txt, preprocess, build_vocab, indexToSentence, find_vocab
from .model import reRNN
import tensorflow as tf

if __name__ == "__main__":
    PATH = "models"
    sess = tf.Session()
    data = read_txt('novel.txt')
    data = preprocess(data)
    vocab, reverse_vocab, vocab_size = build_vocab(data)
    model = reRNN(sess=sess, name="reRNN", max_step=50, vocab_size=vocab_size)
    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint(PATH))
    while(True):
        character = input('세 글자를 입력하세요: ')
        if character == "exit":
            break
        chars = list(character)
        if len(chars) != 3:
            print("세 글자를 입력해 주세요.")
            continue
        for character in chars:
            number = find_vocab(character, vocab)
            if number == "retry":
                continue
            result = model.inference([number])
            print(reverse_vocab[number] + ' ' + indexToSentence(result, reverse_vocab)[0])
        print('')