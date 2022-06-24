import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models

# 闲聊
try:
    cred = credential.Credential("", "")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "nlp.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

    req = models.ChatBotRequest()
    params = {
        "Flag": 0,
        "Query": "你能行不？要不算了吧"
    }
    req.from_json_string(json.dumps(params))

    resp = client.ChatBot(req)
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)

# 情感判断

try:
    cred = credential.Credential("", "")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "nlp.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

    req = models.SentimentAnalysisRequest()
    params = {
        "Text": "你是真能bb啊，你家在黄土高坡啊",
        "Flag": 0,
        "Mode": "2class"
    }
    req.from_json_string(json.dumps(params))

    resp = client.SentimentAnalysis(req)
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)