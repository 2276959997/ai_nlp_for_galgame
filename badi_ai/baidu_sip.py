from app_interface.i_senticment import SenticMent, Emotion, BuildAiException, HandleAiRetException
from aip import AipNlp


class BaiDuAi(SenticMent):
    """需要配置BaiDuAi"""
    conf = ['app_id', 'app_key', 'securet_key']

    def __init__(self, **kwargs):
        """
        传入config 构造BaiDuAi类
        :param kwargs: 要包含 'app_id', 'app_key', 'securet_key'
        """
        for conf_key in BaiDuAi.conf:
            if conf_key in kwargs.keys():
                setattr(self, conf_key, kwargs[conf_key])
            else:
                msg = f'{conf_key} is not found in kwargs for baidu ai'
                raise BuildAiException(msg)

        self.client = AipNlp(self.app_id, self.app_key, self.securet_key)

        # 尝试调用，失败抛出异常
        r_a = self.client.sentimentClassify('test msg')
        r_b = self.client.emotion('test msg')
        if 'error_code' in (str(r_a) + str(r_b)):
            raise BuildAiException("Baidu ai sentimentClassify无法调用，请检查./app.ini 或 *.ini 配置是否正确")

        if 'model' in kwargs:
            self.model = kwargs['model']
        else:
            self.model = 'all'

    def get_str_classify(self, str_):
        """
        返回 文本情绪判断
        :param str_: 要判断的文本
        :return: emotion_typ Emotion的枚举，confidence 可信程(0-1), r_b[2] 更详细的标签(angry, like等), r_b[3] 回复句

        single 模式下，只调用 emotion() 接口
        """

        if self.model == 'single':
            r_b = self.client.emotion(str_, {'scene': 'talk'})
            r_b = BaiDuAi.handle_emotion(r_b)
            return r_b[0].value, r_b[1], r_b[2], r_b[3]

        r_a = self.client.sentimentClassify(str_)
        r_a = BaiDuAi.handle_classify(r_a)
        r_b = self.client.emotion(str_, {'scene': 'talk'})
        r_b = BaiDuAi.handle_emotion(r_b)

        emotion_typ = None
        if r_a[1] > r_b[1]:
            emotion_typ = r_a[0]
            confidence = r_a[1]
        else:
            emotion_typ = r_b[0]
            confidence = r_b[1]
        return emotion_typ.value, confidence, r_b[2], r_b[3]

    @classmethod
    def handle_classify(cls, classify):
        """
        处理百度 sentimentClassify 返回的分析
        :param classify: {'log_id': 2633473275110454486, 'text': '这真的是个不错的选择', 'items': [{'positive_prob': 0.99874, 'confidence': 0.9972, 'negative_prob': 0.00126023, 'sentiment': 2}]}
        :return: emotion_type Emotion枚举, confidence 可信程度
        """
        for key in ['items', 'prob', 'positive', 'negative', 'confidence']:
            if key in str(classify):
                pass
            else:
                raise HandleAiRetException(f'baidu ai 返回中缺少参数 {key}')

        emotion_type = None
        positive = classify['items'][0]['positive_prob']  # 消极
        negative = classify['items'][0]['negative_prob']  # 积极
        confidence = classify['items'][0]['confidence']  # 置信度
        if positive >= negative:
            emotion_type = Emotion.POSITIVE
        else:
            emotion_type = Emotion.NEGATIVE
        return emotion_type, confidence

    @classmethod
    def handle_emotion(cls, emotion):
        """
        emotion 接口返回消息处理
        :param emotion: emotion返回消息
        :return:emotion_type Emotion枚举, confidence 综合置信度, sub_label 更详细的标签, replies 回复
        """
        for key in ['items', 'label', 'prob', 'subitems']:
            if key in str(emotion):
                pass
            else:
                raise HandleAiRetException(f'baidu ai 返回中缺少参数 {key}')

        emotion_type = None
        label = emotion['items'][0]['label']
        confidence = emotion['items'][0]['prob']
        if len(emotion['items'][0]['subitems']) != 0:
            sub_label = emotion['items'][0]['subitems'][0]['label']
            replies = emotion['items'][0]['replies'][0]
        else:
            sub_label = ''
            replies = ''

        # 判断情绪标签
        if label == 'pessimistic':
            emotion_type = Emotion.POSITIVE
        if label == 'neutral':
            emotion_type = Emotion.NEUTRAL
        if label == 'optimistic':
            emotion_type = Emotion.NEGATIVE

        return emotion_type, confidence, sub_label, replies
