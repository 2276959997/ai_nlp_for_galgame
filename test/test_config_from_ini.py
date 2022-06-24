from utils.config_from_ini import ConfigFromIni
import unittest
import os


class TestConfigFromIni(unittest.TestCase):
    """config 测试"""
    def test_init(self):
        """传参不存在路径"""
        path = os.getcwd() + "111"
        self.assertRaises(FileNotFoundError, ConfigFromIni, path=path)

    def test_init_no_path(self):
        """缺省测试"""
        conf = ConfigFromIni()
        path = os.path.join(os.path.split(os.getcwd())[0], 'app.ini')
        self.assertEqual(conf.path, path)

    def test_instance__dict__(self):
        """参数验证"""
        conf = ConfigFromIni()
        self.assertEqual(conf._config.get('baidu', 'app_id'), conf.baidu.app_id)


if __name__ == '__main__':
    unittest.main()


