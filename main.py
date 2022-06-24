import asyncio
import websockets
import json

from utils.config_factory import GetConfig
from app_interface.senticment_factory import GetAi


# 获取项目配置
config = GetConfig.get_config('ini_config')
# 实例化一个ai
ai = GetAi.get_ai(config)
# 游戏客户端集合
GAME_CLIENT = set()


async def ai_output(websocket):
    global GAME_CLIENT
    async for msg in websocket:
        msg = str(msg).encode('utf-8').decode("unicode_escape")
        msg = json.loads(msg)
        if 'MsgEvet' in msg:
            event = msg['MsgEvet']
            # TODO 返回分装成接口
            if event == 'str_emotion_classify':
                send_msg = ai.get_str_classify(msg['MsgText'])

                send_msg_dic = dict()
                send_msg_dic['emotion_type'] = send_msg[0]
                send_msg_dic['confidence'] = send_msg[1]
                send_msg_dic['sub_label'] = send_msg[2]
                send_msg_dic['replies'] = send_msg[3]

                print(json.dumps(send_msg_dic).encode('utf-8').decode("unicode_escape"))
                await websocket.send(json.dumps(send_msg_dic))
        else:
            await websocket.send('unknow message')


async def main():
    async with websockets.serve(ai_output, '', 16666):
        # run forever
        await asyncio.Future()


if __name__ == '__main__':

    # 根据项目根目录的app.ini实例化一个ai对象
    # ai = GetAi.get_ai(config)

    # 调用ai获得分析
    # (1, 0.999998, 'angry', '稍安勿躁哦')
    # 1 Emotion枚举
    # 0.99998 综合置信度
    # 'angry' 更详细标签(具体多少个我也不知道)
    # ‘稍安勿躁哦' 回复语句
    # print(ai.get_str_classify('滚呐，贱人'))

    asyncio.run(main())
