from flask import Flask, request

from kakaoplus import KaKaoAgent
from engines import YosEngine, HosEngine

app = Flask(__name__)
KaKao = KaKaoAgent()


@app.route('/keyboard', methods=['GET'])
def keyboard_handler():
    data = request.args.get('data')
    # res = KaKao.handle_keyboard_webhook()
    text = HosEngine().activate(data)

    return text


@app.route('/message', methods=['POST'])
def message_handler():
    req = request.get_data(as_text=True)
    res = KaKao.handle_webhook(req)

    return res


@KaKao.handle_keyboard
def keyboard_handler(res):
    '''
    :param req: request from kakao
    :param res: response
    '''
    res.keyboard_buttons = [
        'button1',
        'button2',
        'button3'
    ]


@KaKao.handle_message
def handle_message(req, res):
    '''
    :param req: request from kakao
    :param res: response
    '''
    echo_message = req.content

    res.text = "Echo Message: " + echo_message


@KaKao.handle_message(['hello', 'hi'])
def greeting_callback(req, res):
    '''
    :param req: request from kakao
    :param res: response
    '''
    res.text = "안녕 :)"


@KaKao.handle_message(['(^yo.*)'])
def use_yo_engine(req, res):
    text = req.content[-1]
    res.text = YosEngine().activate(text)


if __name__ == "__main__":
    app.run()