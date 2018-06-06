from flask import Flask, request

from kakaoplus import KaKaoAgent
from engines import YosEngine, HosEngine

app = Flask(__name__)
KaKao = KaKaoAgent()


@app.route('/keyboard', methods=['GET'])
def keyboard_handler():
    res = KaKao.handle_keyboard_webhook()

    return res


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
        '삼행시 시작',
        '사용법 보기'
    ]


@KaKao.handle_message
def handle_message(req, res):
    '''
    :param req: request from kakao
    :param res: response
    '''
    data = req.content
    if len(data) > 3:
        text= "3글자가 넘어가면 안됩니다."
    else:
        text = HosEngine().activate(data)

    res.text = text


@KaKao.handle_message(['삼행시 시작, 시작'])
def start_message(req, res):
    text = "삼행시를 시작합니다! 3글자만 말해주세요!"
    res.text = text


@KaKao.handle_message(['사용법 보기', '사용법'])
def creator_info(req, res):
    text = "3글자 미만을 말하시면 됩니다."
    res.text = text


if __name__ == "__main__":
    app.run()