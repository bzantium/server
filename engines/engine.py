from abc import ABCMeta, abstractclassmethod

class Engine(metaclass=ABCMeta):
    """
    Engine들이 상속해야하는 metaclass 입니다.
    """
    @abstractclassmethod
    def activate(self, text):
        pass