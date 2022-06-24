"""
单独调用示例
"""

from utils.config_factory import GetConfig
from badi_ai.baidu_sip import BaiDuAi

if __name__ == '__main__':
    config = GetConfig.get_config('ini_config')

    # 根据项目根目录的app.ini实例化一个ai对象
    ai = BaiDuAi(app_id=config.baidu.app_id, app_key=config.baidu.app_key,
                                    securet_key=config.baidu.securet_key)

    # 调用ai获得分析
    # (1, 0.999998, 'angry', '稍安勿躁哦')
    # 1 Emotion枚举
    # 0.99998 综合置信度
    # 'angry' 更详细标签(具体多少个我也不知道) 可能为''
    # ‘稍安勿躁哦' 回复语句                  可能为''

    # print(ai.get_str_classify("这一辈子，你有没有为谁拼过命啊！"))
    # print(ai.get_str_classify("如果不在相见，你余生苦难的日子里会不会再想起我来"))
    # print(ai.get_str_classify("不要再说喜欢我了，你这个骗子"))
    # print(ai.get_str_classify("你怎么可以这样对我，难道我给的还不够多吗"))
    print(ai.get_str_classify("我懂了，你就是故意的，你怎么可以这样对我"))

    # (2, 0.995217, 'disgusting', '对不起，我会继续努力')