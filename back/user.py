from db import mongo_client, redis_client
from encrypt import AES_en, AES_de

'''
    cookie:
        {'user_id': '', 'user_type': '', 'expire_time': ''}
'''


# 获取公众号登陆qr
import requests
import json


def create_qrcode_ticket(access_token, scene_id, temporary=True):
    url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=" + access_token
    if temporary:
        data = {
            "expire_seconds": 604800,  # 7 days
            "action_name": "QR_SCENE",
            "action_info": {"scene": {"scene_id": scene_id}}
        }
    else:
        data = {
            "action_name": "QR_LIMIT_SCENE",
            "action_info": {"scene": {"scene_id": scene_id}}
        }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["ticket"]
    else:
        raise Exception("Failed to create QR code ticket: " + response.text)


def get_qrcode_image(ticket):
    url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=" + ticket
    response = requests.get(url)
    if response.status_code == 200:
        with open("qrcode.jpg", "wb") as f:
            f.write(response.content)
    else:
        raise Exception("Failed to get QR code image: " + response.text)




# 检查token合法性
def check_token(token: str):
    try:
        r = AES_de(token)
        r['user_id']
        r['user_type']
        r['expire_time']
        return True
    except:
        return False


# 注册
def register():
    pass


# 登陆
def login():
    pass


# 获取用户信息
def get_user_info():
    pass


# 获取用户额度信息
def get_user_token():
    pass


# 获取用户订单信息
def get_user_bill():
    pass


# 获取会员充值信息
def get_user_level():
    pass


