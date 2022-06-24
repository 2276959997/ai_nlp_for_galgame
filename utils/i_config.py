from abc import abstractmethod
from abc import ABCMeta


class ReadConfig(metaclass=ABCMeta):

    @abstractmethod
    def get_config(self):
        pass



