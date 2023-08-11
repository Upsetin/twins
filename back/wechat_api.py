import asyncio
import json
import time
import urllib.parse
import xml.etree.ElementTree as ET

import httpx
import openai
import redis
import requests
from loguru import logger

from db import MongoClient

openai.api_key = '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'  # 替换为你的 OpenAI API 密钥
openai.api_base = 'http://bitorgin.cn/v1'


async def ask_question(question: str):
    messages = [
        {'role': 'system',
         'content': "Answer questions as friendly and detailed as possible. If there are no special requirements, please answer in Chinese"},
        {"role": "user", "content": question},
    ]

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        max_tokens=666,
        n=1,
        stop=None,
        temperature=0.7
    )

    print(response)

    return response["choices"][0]["message"]["content"]


# 用于官网api的专用函数
def ask_question_raw_data(question_list: list):
    # 查询缓存

    messages = [
        {'role': 'system',
         'content': "Answer questions as friendly and detailed as possible. If there are no special requirements, please answer in Chinese"},

        # {"role": "user", "content": question},
    ]

    # 添加历史聊天内容
    for i in question_list:
        messages.append(i)

    response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-3.5-turbo-0613",
        messages=messages,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7
    )

    # 设置缓存

    return response


# 主动回复消息
async def send_user_msg(openid: str, content: str):
    access_token = await get_access_token()
    url = f'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={access_token}'

    data = {
        "touser": openid,
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
        # r = r.json()

    print(r.json())


# # 示例调用
# question = "你好，请问100年前的中国是怎么样的呢，如果我想学习如何控制面部表情，请问我需要怎么做"
#
# response = ask_question(question)
# print(response)


# 必要信息
appid = 'wxe59bf8bfee088d72'
app_secret = '6a03758acc1cbb63bcad112f54261868'


# 获取token
async def get_access_token(update=True):
    # 将重要信息存入redis -> 提取token
    logger.info('正在获取access_token...')
    redis_client = redis.Redis(host='8.222.210.54', password='Klx5596688')
    access_token = redis_client.hget('wechat:data', 'access_token')
    logger.debug(f'读取到token: {access_token}')
    if access_token and update == False:
        access_token = access_token.decode()
        return access_token

    logger.info("正在获取微信access_token...")
    # url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={app_secret}'
    url = 'https://api.weixin.qq.com/cgi-bin/stable_token'
    data = {
        'grant_type': 'client_credential',
        'appid': appid,
        'secret': app_secret,
        'force_refresh': False
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=data)
        r = r.json()
        logger.debug(f'「返回结果」获取微信access_token|{r}')
    access_token = r['access_token']
    logger.success(f'获取成功! access_token: {access_token}')
    # 更新token
    redis_client.hset('wechat:data', 'access_token', access_token)
    logger.success(f'已更新redis数据: 「HASH」| wechat:data -> access_token = {access_token}')
    return access_token


# 获取qr
async def get_qrcode(scene_str: str = ''):
    # 获取 access_token
    access_token = await get_access_token()
    url = f'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={access_token}'
    data = {
        # 5min超时时间
        'expire_seconds': 5 * 60,
        # 临时参数二维码
        'action_name': 'QR_STR_SCENE',
        # action_info
        'action_info': {
            "scene":
                {
                    "scene_str": scene_str
                }
        },
    }

    # 传参数, 获取 ticket
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=data)
        logger.debug(f'「返回结果」获取带参数二维码ticket|{r}|{r.text}')

        # token过期
        if r.json().get('errcode', '') in [40001, 42001]:
            logger.error('access_token已过期,正在重新获取...')
            # 递归调用
            return await get_qrcode(scene_str)

        print(r.json())
        ticket = r.json()['ticket']

        # 获取二维码
        param = {
            'ticket': ticket
        }

        url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?' + urllib.parse.urlencode(param)

        logger.success(f'已获取二维码!|{url}')

        return url, ticket
        # async with httpx.AsyncClient() as client:
        #     r = await client.get(url)
        #     logger.debug(f'「返回结果」ticket二维码状态|{r}')
        #     with open('test.jpg', 'wb') as f:
        #         f.write(r.content)
        # logger.success(f'已获取二维码!|{ticket}')


# 处理
async def process_answer_message(openid: str, content: str) -> None:
    # 在这里根据用户发送的文本消息进行逻辑处理，生成回复内容
    # 示例中仅返回一个固定的回复内容
    # 引用GPT回复

    # 判断额度
    # 获取token
    base_info = MongoClient(collection_name='user_base_info').find({'openid': openid}, only_one=True)
    if base_info['token'] <= 0 and base_info['user_type'] == 'vip':
        reply_content = '试用额度已使用完，请订阅会员后重试~\n\n限时优惠🔥仅需¥35!\n\n<a href="https://chat.multicosmo.com">点击前往官网进行升级</a>\n\n升级指南: 页面侧边栏->订阅会员(Upgrade)->选择方案升级'
    else:
        answer = await ask_question(content)

        # reply_content = answer + '\n\n' + '————————————————\n「以上内容由<a href="https://chat.multicosmo.com">ChatGPT</a>生成」\n\n\n<a href="https://chat.multicosmo.com" style="color: red;">试用即将结束，请及时订阅升级！</a>'

        if base_info['user_type'] == 'vip':
            reply_content = answer + '\n\n\n' + '<a href="https://chat.multicosmo.com" style="color: red;">注意:请及时订阅升级！</a>\n' + '————————————————\n「以上内容由<a href="https://chat.multicosmo.com">ChatGPT</a>生成」'
        else:
            reply_content = answer + '\n\n\n' + '————————————————「以上内容由<a href="https://chat.multicosmo.com">ChatGPT</a>生成」'

    await send_user_msg(openid, reply_content)


# 获取用户信息
async def get_user_info(openid: str) -> dict:
    url = f"https://api.weixin.qq.com/cgi-bin/user/info?access_token={await get_access_token()}&openid={openid}&lang=zh_CN"
    response = requests.get(url)
    user_info = response.json()

    return user_info


if __name__ == '__main__':
    start_time = time.time()
    r = asyncio.run(ask_question("请用python写一个贪吃虫游戏"))
    print(r)
    print(f'cost time: {time.time() - start_time}')
    # token = asyncio.run(get_access_token())
    # token = '70_hpMuUCnLdNIcxIkMNYwMm8z9yTM9DxLgL_Tm8Gxf07beFV8DXCakLpmTHOXhoj5LY6XdZ2luqY21FChxcquMgEoyi5vc4qt2kNLZLGH4fIACavRntrvEcRVYbRgPQCjAFABCO'
    # r = asyncio.run(get_qrcode())
    # print(r)
