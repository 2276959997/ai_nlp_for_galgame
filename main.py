import asyncio
import websockets
import json
import chardet

from utils.config_factory import GetConfig
from app_interface.senticment_factory import GetAi

# 获取项目配置
config = GetConfig.get_config('ini_config')
# 实例化一个ai
ai = GetAi.get_ai(config)
# 游戏客户端集合
GAME_CLIENT = set()


def handle_msg(msg):
    """预处理msg"""
    # 如果是b'’就单程unicode来处理
    is_bytes = False
    if isinstance(type(msg), type(bytes)):
        msg = msg.decode('unicode-escape')
        is_bytes =True
    try:
        msg = json.loads(msg)
    except json.decoder.JSONDecodeError as JErr:
        print(f"不能序列化为json的字符串{msg}")
    finally:
        pass

    return is_bytes, isinstance(type(msg), type(dict)), msg


async def ai_output(websocket):
    global GAME_CLIENT

    async for msg in websocket:
        is_bytes, is_dict, msg = handle_msg(msg)

        # dict类型，json.loads成功
        if is_dict:
            # 非字符串
            if 'MsgEvent' in msg.keys():
                event = msg['MsgEvent']
                # TODO 返回分装成接口
                if event == 'strEmotionClassify':
                    send_msg = ai.get_str_classify(msg['MsgText'])

                    send_msg_dic = dict()
                    send_msg_dic['emotionType'] = send_msg[0]
                    send_msg_dic['confidence'] = send_msg[1]
                    send_msg_dic['subLabel'] = send_msg[2]
                    send_msg_dic['replies'] = send_msg[3]

                    # print("return c#: ", json.dumps(send_msg_dic).encode('utf-8').decode("unicode_escape"))
                    if is_bytes:
                        await websocket.send(json.dumps(send_msg_dic).encode('utf-8').decode("unicode_escape"))
                    else:
                        await websocket.send(json.dumps(send_msg_dic))

            else:
                send_msg_dic = dict()
                send_msg_dic['err'] = "unknown message"
                if is_bytes:
                    await websocket.send(json.dumps(msg).encode('utf-8').decode("unicode_escape"))
                else:
                    await websocket.send(json.dumps(msg))
        else:
            await websocket.send(msg)


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
