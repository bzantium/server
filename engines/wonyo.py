from .engine import Engine

class YosEngine(Engine):
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
        return "아직 준비중인 엔진입니다."