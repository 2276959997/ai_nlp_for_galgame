from abc import abstractmethod
from abc import ABCMeta
from enum import Enum


class BuildAiException(Exception):
    """AI 类构造异常"""
    def __init__(self, msg):
        self.msg = msg


class HandleAiRetException(Exception):

    def __init__(self, msg):
        self.msg = msg

class Emotion(Enum):
    POSITIVE = 1    # 消极
    NEGATIVE = 2    # 积极
    NEUTRAL = 3     # 中性


class SenticMent(metaclass=ABCMeta):

    @abstractmethod
    def get_str_classify(self, str_):
        pass


