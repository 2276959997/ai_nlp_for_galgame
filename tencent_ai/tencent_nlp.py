import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models

from app_interface.i_senticment import SenticMent, Emotion, BuildAiException, HandleAiRetException


class TencentAi(SenticMent):
    """需要配置TencentAi"""
    conf = ['secret_id', 'secret_key']

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        for conf_key in TencentAi.conf:
            if conf_key in kwargs.keys():
                setattr(self, conf_key, kwargs[conf_key])
            else:
                msg = f'{conf_key} is not found in kwargs for tencent ai'
                raise BuildAiException(msg)

        try:
            cred = credential.Credential(self.secret_id, self.secret_key)
            self.cred = cred

            httpProfile = HttpProfile()
            self.httpProfile = httpProfile

            httpProfile.endpoint = "nlp.tencentcloudapi.com"

            clientProfile = ClientProfile()
            self.clientProfile = clientProfile

            clientProfile.httpProfile = httpProfile
            self.client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

            # 尝试调用，失败抛出异常
            req = models.ChatBotRequest()
            params = {
                "Flag": 0,
                "Query": "test one"
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.ChatBot(req)
            # print(resp.to_json_string())
        except TencentCloudSDKException as err:
            msg = err
            raise BuildAiException(msg)

    def get_str_classify(self, str_):
        # 获得情感分类
        req_classify = models.SentimentAnalysisRequest()
        params = {
            "Text": str_,
            "Flag": 0,
            "Mode": "2class"
        }
        req_classify.from_json_string(json.dumps(params))
        resp_classify = self.client.SentimentAnalysis(req_classify)
        r_a = TencentAi.handle_classify(resp_classify)

        # 获得回复
        req_chat = models.ChatBotRequest()
        params = {
            "Flag": 0,
            "Query": str_
        }
        req_chat.from_json_string(json.dumps(params))
        resp_chat = self.client.ChatBot(req_chat)
        r_b = TencentAi.handle_emotion(resp_chat)
        return r_a[0].value, r_a[1], '', r_b[0]

    @classmethod
    def handle_classify(cls, classify):
        """
        emotion 接口返回消息处理
        :param classify:
        :return: emotion_type Emotion枚举, confidence置信度
        """
        for key in ['Positive', 'Neutral', 'Negative', 'Sentiment']:
            if key in str(classify):
                pass
            else:
                raise HandleAiRetException(f'baiu ai 返回中缺少参数 {key}')

        emotion_type = None
        positive = classify.Positive
        negative = classify.Negative
        confidence = 0
        if positive > negative:
            emotion_type = Emotion.POSITIVE
            confidence = positive
        else:
            emotion_type = Emotion.NEGATIVE
            confidence = negative
        return emotion_type, confidence

    @classmethod
    def handle_emotion(cls, emotion):
        """
        emotion 接口返回消息处理
        :param emotion: emotion返回消息
        :return:replies 回复, confidence 综合置信度
        """
        for key in ['Reply', 'Confidence', 'RequestId']:
            if key in str(emotion):
                pass
            else:
                raise HandleAiRetException(f'baidu ai 返回中缺少参数 {key}')
        replies = emotion.Reply
        confidence = emotion.Confidence

        return replies, confidence