from app_interface.i_senticment import SenticMent
from badi_ai.baidu_sip import BaiDuAi
from tencent_ai.tencent_nlp import TencentAi


class GetAi:
    @classmethod
    def get_ai(cls, conf):
        ai_object = None
        if 'global_' in conf.__dict__.keys() and 'ai_choose' in conf.__dict__['global_'].__dict__:
            if conf.global_.ai_choose == 'baidu':
                ai_object = BaiDuAi(app_id=conf.baidu.app_id, app_key=conf.baidu.app_key,
                                    securet_key=conf.baidu.securet_key)
            if conf.global_.ai_choose == 'tencent':
                ai_object = TencentAi(secret_id=conf.tencent.secret_id, secret_key=conf.tencent.secret_key)

        if ai_object:
            return ai_object
        else:
            raise Exception("app.ini中参数'[global_] ai'缺失或错误，无法选定使用哪个ai")