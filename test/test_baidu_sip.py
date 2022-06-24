from badi_ai.baidu_sip import BaiDuAi, BuildAiException, HandleAiRetException
import unittest


class TestBaiDuAi(unittest.TestCase):
    """传参异常 处理检查"""
    def test_cls_handle_classify(self):
        """错误参数测试"""
        source_data = list()
        self.assertRaises(HandleAiRetException, BaiDuAi.handle_classify, source_data)

    def test_cls_handle_emotion(self):
        """错误参数测试"""
        source_data = list()
        self.assertRaises(HandleAiRetException, BaiDuAi.handle_emotion, source_data)

    def test_raise(self):
        """错误参数测试"""
        app_id = '111'
        app_key = "222"
        securet_key = "333"
        self.assertRaises(BuildAiException, BaiDuAi, app_id=app_id, app_key=app_key, securet_key=securet_key, path=None)


if __name__ == '__main__':
    unittest.main()