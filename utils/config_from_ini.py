from utils.i_config import ReadConfig
import configparser
import os


class SObject(dict):

    def set_attr(self, key, value):
        setattr(self, key, value)
        return self


class ConfigFromIni(ReadConfig):
    """
    从上一层目录的app.ini配置文件初始化项目配置
    """

    def __init__(self, **kwargs):
        self.path = None
        # 判断是否传参了
        if 'path' in kwargs.keys():
            if kwargs['path'].endswith('.ini') and os.path.exists(kwargs['path']):
                self.path = kwargs['path']
            else:
                raise FileNotFoundError("找不到以.ini结尾的配置文件 或 配置文件不存在")
        path = os.path.join(os.getcwd(), 'app.ini')
        # 未传参是否在当前目录下有app.ini
        if not self.path and os.path.exists(path):
            self.path = path
        path = os.path.join(os.path.split(os.getcwd())[0], 'app.ini')
        # 是否在上层目录有app.ini
        if not self.path and os.path.exists(path):
            self.path = path
        # 都没有抛出异常
        if not self.path:
            raise FileNotFoundError(f'{path} not include file: app.ini')

        self._config = None
        self.read_config()

    def read_config(self):
        self._config = configparser.ConfigParser()
        self._config.read(self.path, encoding='utf-8')

        for section in self._config.sections():
            s_o = SObject()
            for option in self._config.options(section):
                s_o.set_attr(option, self._config.get(section, option))
            setattr(self, section, s_o)

    def get_config(self):
        """抽象类实现"""
        return self


# conf = ConfigFromIni()
# conf.get_config()
# print(conf.__dict__)