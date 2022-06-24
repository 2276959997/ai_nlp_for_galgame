from utils.config_factory import GetConfig
from tencent_ai.tencent_nlp import TencentAi

if __name__ == '__main__':
    config = GetConfig.get_config()

    ai = TencentAi(secret_id=config.tencent.secret_id, secret_key=config.tencent.secret_key)
    print(ai.get_str_classify('我懂了，你就是故意的，你怎么可以这样对我'))

    # tencent:  (2, 0.69013831, '', '可能刚刚不在一个频道，待我调频哈')
    # baidu:    (2, 0.995217, 'disgusting', '对不起，我会继续努力')