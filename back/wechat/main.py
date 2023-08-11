import asyncio
import time
import urllib.parse

from loguru import logger

import wechat
import httpx

from db import redis_client

# 必要信息
appid = 'wxe59bf8bfee088d72'
app_secret = '6a03758acc1cbb63bcad112f54261868'


# 将重要信息存入redis -> 提取token
token = redis_client.hget('wechat:data', 'access_token')
logger.debug(f'读取到token: {token}')
if token:
    token = token.decode()


async def get_access_token():
    logger.info("正在获取微信access_token...")
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={app_secret}'
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        r = r.json()
        logger.debug(f'「返回结果」获取微信access_token|{r}')
    access_token = r['access_token']
    logger.success(f'获取成功! access_token: {access_token}')
    # 更新token
    redis_client.hset('wechat:data', 'access_token', access_token)
    logger.success(f'已更新redis数据: 「HASH」| wechat:data -> access_token = {access_token}')
    return access_token


async def get_qrcode(access_token: str = ''):
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
                    "scene_str": str(time.time())
                }
        },
    }

    # 传参数, 获取ticket
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=data)
        logger.debug(f'「返回结果」获取带参数二维码ticket|{r}')

        # token过期
        if r.json().get('errcode', '') == 40001:
            logger.error('access_token已过期,正在重新获取...')
            # 新获取token
            access_token = await get_access_token()
            # 更新token
            redis_client.hset('wechat:data', 'access_token', access_token)
            logger.success(f'已更新redis数据: 「HASH」| wechat:data -> access_token = {access_token}')
            # 递归调用
            return await get_qrcode(access_token)

        print(r.json())
        ticket = r.json()['ticket']

        # 获取二维码
        param = {
            'ticket': ticket
        }

        url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?' + urllib.parse.urlencode(param)
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            logger.debug(f'「返回结果」ticket二维码状态|{r}')
            with open('test.jpg', 'wb') as f:
                f.write(r.content)
        logger.success(f'已获取二维码!|{ticket}')


if __name__ == '__main__':
    # token = asyncio.run(get_access_token())
    # token = '70_hpMuUCnLdNIcxIkMNYwMm8z9yTM9DxLgL_Tm8Gxf07beFV8DXCakLpmTHOXhoj5LY6XdZ2luqY21FChxcquMgEoyi5vc4qt2kNLZLGH4fIACavRntrvEcRVYbRgPQCjAFABCO'
    asyncio.run(get_qrcode(token))
