# 微信支付商户号，服务商模式下为服务商户号，即官方文档中的sp_mchid。
import logging
import os
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import json
import logging
import os
from random import sample
from string import ascii_letters, digits

from wechatpayv3 import SignType, WeChatPay, WeChatPayType


MCHID = '1647822871'

# 商户证书私钥，此文件不要放置在下面设置的CERT_DIR目录里。
with open('cert/apiclient_key.pem') as f:
    PRIVATE_KEY = f.read()

# 商户证书序列号
CERT_SERIAL_NO = '17EF188D8651DC93D0E5BD43DB9C8CA03A75B50F'
# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
APIV3_KEY = 'erJX2M9iZEeGXCl29zu2qTCuwWF2b7P4'
# APPID，应用ID，服务商模式下为服务商应用ID，即官方文档中的sp_appid，也可以在调用接口的时候覆盖。
APPID = 'wxe59bf8bfee088d72'
# 回调地址，也可以在调用接口的时候覆盖。
NOTIFY_URL = 'https://api.multicosmo.com/wechat/payment'
# 微信支付平台证书缓存目录，初始调试的时候可以设为None，首次使用确保此目录为空目录。
CERT_DIR = './cert'
# 日志记录器，记录web请求和回调细节，便于调试排错。
logging.basicConfig(filename=os.path.join(os.getcwd(), 'demo.log'), level=logging.DEBUG, filemode='a', format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger("demo")
# 接入模式：False=直连商户模式，True=服务商模式。
PARTNER_MODE = False
# 代理设置，None或者{"https": "http://10.10.1.10:1080"}，详细格式参见https://docs.python-requests.org/zh_CN/latest/user/advanced.html
PROXY = None


wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.NATIVE,
    mchid=MCHID,
    private_key=PRIVATE_KEY,
    cert_serial_no=CERT_SERIAL_NO,
    apiv3_key=APIV3_KEY,
    appid=APPID,
    notify_url=NOTIFY_URL,
    cert_dir=CERT_DIR,
    logger=LOGGER,
    partner_mode=PARTNER_MODE,
    proxy=PROXY)

app = FastAPI()

@app.get('/pay/{amount}')
def pay(amount: int):
    # 以native下单为例，下单成功后即可获取到'code_url'，将'code_url'转换为二维码，并用微信扫码即可进行支付测试。
    out_trade_no = str(int(time.time()*1000))
    description = 'wechat payment test'
    # amount = 1
    print(amount, type(amount))
    # amount = 1
    code, message = wxpay.pay(
        description=description,
        out_trade_no=out_trade_no,
        amount={'total': amount},
        pay_type=WeChatPayType.NATIVE
    )
    message = json.loads(message)
    return JSONResponse(content={'code': code, 'message': message})


if __name__ == '__main__':
    out_trade_no = 'test0001'
    description = 'wechat payment test'
    amount = 1
    code, message = wxpay.pay(
        description=description,
        out_trade_no=out_trade_no,
        amount={'total': amount},
        pay_type=WeChatPayType.NATIVE
    )
    message = json.loads(message)
    print(message)
    uvicorn.run(app, host="localhost", port=80)
