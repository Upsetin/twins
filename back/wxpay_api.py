# 微信支付商户号，服务商模式下为服务商户号，即官方文档中的sp_mchid。

import json
import logging
import os
import random
import time
from string import ascii_letters, digits

from wechatpayv3 import WeChatPay, WeChatPayType

from func import make_qr_img

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
logging.basicConfig(filename=os.path.join(os.getcwd(), 'demo.log'), level=logging.DEBUG, filemode='a',
                    format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
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


def wx_pay(amount: int, out_trade_no: str = '商家订单号', description: str = '描述', pay_type: str = 'NATIVE',
           payer_openid: str = 'oB4qP6eXuFoEEz_61EGXlDrR9LlQ'):
    # 以native下单为例，下单成功后即可获取到'code_url'，将'code_url'转换为二维码，并用微信扫码即可进行支付测试。
    # out_trade_no = str(int(time.time()*1000))
    # description = 'wechat payment test'
    # amount = 1
    # print(amount, type(amount))
    # amount = 1
    if pay_type == 'NATIVE':
        code, message = wxpay.pay(
            description=description,
            out_trade_no=out_trade_no,
            amount={'total': amount},
            pay_type=WeChatPayType.NATIVE
        )
        message = json.loads(message)

        print(message)

        if code == 200:
            qr_base64 = make_qr_img(message['code_url'])
            return {'code': 200, 'qr_base64': qr_base64}
        else:
            return {'code': 500, 'msg': message['message']}
    # JSAPI
    else:
        description = description
        payer = {'openid': payer_openid}

        print("amount JSAPI:", amount)
        code, message = wxpay.pay(
            description=description,
            out_trade_no=out_trade_no,
            amount={'total': amount},
            pay_type=WeChatPayType.JSAPI,
            payer=payer
        )
        result = json.loads(message)
        if code in range(200, 300):
            prepay_id = result.get('prepay_id')
            timestamp = str(int(time.time() * 1000))
            noncestr = ''.join(random.choices('qwertyuiopasdghjklzxcvbnmm1234567890QWERTYUIOPASDFGHJKLZXCVBNM',
                                              k=random.randint(1, 30)))
            package = 'prepay_id=' + prepay_id
            paysign = wxpay.sign([APPID, timestamp, noncestr, package])
            signtype = 'RSA'
            return {'code': 200, 'result': {
                'appId': APPID,
                'timeStamp': timestamp,
                'nonceStr': noncestr,
                'package': 'prepay_id=%s' % prepay_id,
                'signType': signtype,
                'paySign': paysign
            }}
        else:
            return {'code': -1, 'result': {'reason': result.get('code')}}


def pay_jsapi():
    # 以jsapi下单为例，下单成功后，将prepay_id和其他必须的参数组合传递给JSSDK的wx.chooseWXPay接口唤起支付
    out_trade_no = ''.join(random.sample(ascii_letters + digits, 8))
    description = 'demo-description'
    amount = 1
    payer = {'openid': 'demo-openid'}
    code, message = wxpay.pay(
        description=description,
        out_trade_no=out_trade_no,
        amount={'total': amount},
        pay_type=WeChatPayType.JSAPI,
        payer=payer
    )
    result = json.loads(message)
    if code in range(200, 300):
        prepay_id = result.get('prepay_id')
        timestamp = 'demo-timestamp'
        noncestr = 'demo-nocestr'
        package = 'prepay_id=' + prepay_id
        paysign = wxpay.sign([APPID, timestamp, noncestr, package])
        signtype = 'RSA'
        return {'code': 0, 'result': {
            'appId': APPID,
            'timeStamp': timestamp,
            'nonceStr': noncestr,
            'package': 'prepay_id=%s' % prepay_id,
            'signType': signtype,
            'paySign': paysign
        }}
    else:
        return {'code': -1, 'result': {'reason': result.get('code')}}


def wxpay_calback(headers, body):
    print('headers:', type(headers), headers)
    print('body:', type(body), body)
    r = wxpay.callback(
        headers, body
    )
    print(' wxpay.callback: ', r)
    print(type(r), r)
    return r


def wx_pay_query_bill(out_trade_no: str):
    code, res = wxpay.query(out_trade_no='test0001')
    return code, res


if __name__ == '__main__':
    out_trade_no = str(int(time.time()))
    description = 'wechat payment test'
    amount = 1
    qr_base64 = wx_pay(amount, out_trade_no, description, 'JSAPI')
    print(qr_base64)
    # r = pay_jsapi()
    # print(r)

