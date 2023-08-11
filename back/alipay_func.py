import base64
import json
import time
import urllib.parse
from datetime import datetime

import requests
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from loguru import logger

# 你的支付宝应用的AppId和PrivateKey
app_id = "2021004102603026"
private_key = '''-----BEGIN RSA PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQClXOs6yzqOgu8T
D3SDEuz/B4JxR4FCFDg1sKoU586YFZxtU8dgaO3CEoBzyycZcjZK+30x2ORL/6HC
Lqa4avOH/eu/JjS7SWXWl0e3UKPwfADpyK5r8CfJaSraNmWk9QiQKSh+BhRD0ThA
YZZlocUiirtBYTOnHMYfQ+L/FnrxORV2bO7INLdrpPWkBVYG5+ZR0VKeTJ7skcda
IlrSKLRBQAwlBIa5ZEWBPKbF2D2kgLJxsQOmHo5P5eTjTTKbqNMzYeGSsrkdxOzN
VxVbfgoGb+oj74Nyu6t6mA13OON2riSjbn7KxzxglzmuGA8k0h8O0ZKJDMQ514Nr
xOwplp1RAgMBAAECggEBAJyobbUyaVQvmNx+zMuMN3fYHmzA6CS40ROUPV02ylLs
TliIgR7F6VDthEGu2WjS+bqJjG6X4phZIl67IXke4X4ZQajCQjyX6WGlyexR+i3O
3HKeixd42ciG2HEIDb174dPpGhJiIfqpj9f2W6wG2KLDuWjT9EJCETP3dWpiWrCA
9OkiBk50ipusLwdhdveADeJ/IL9HwIzrEQ6wglbMmoGgZXw4ZqmIjSQmQYS0wF6j
4qQA7+5z3JVMog7r8r0GRZOZ30Zy8UvNOGLR3Ib+lZI6Lu8iqw60oBAEpET3fMUW
/2Er+5Re38gOaGdXVxS6stkwI+ClCCL8wSsOdfcTcn0CgYEA0zgB1rMvC2DyOaO4
WJO+ulg/SK9KoNgVNothPF3k5LnZzM+QE37dU2YrWF6jOUC9AKXXYTAPuU40+1oa
D31QVSJQzk+FTeeOG5pVlZsYHOow1e071R4iDxgAdNJ+LTMqn9YVDF5bdV9n14eV
34Nvk8uJ6zctbz0nKFVt999Xs18CgYEAyGwRKxrUDGrsWYgW7s7vmwUXPDLM1hgZ
ofDTmFkyLat/syH0vLagsl2eiX1LUckZtEuhm7OZJnxEG0bIUEKMOGBGyxzOOwdQ
byPZCDT1LpR8Q12lx907vfQ1wBzgq/HqaIdBwG8TEsYQsTK+RslJWC4tWvIged6S
ubuonGabnU8CgYEAmB7eNCMY3rkTuy+OtTyzQMIN0ettdCosHPyFK1T0ZUb09e0H
dwMHo+kRjrOaGsHlXXITjItwx6Trw5tA6ab3FFmCmRPsjg8W6gpdWUI6O5jvUyNo
1DS/kt9WdMyk0yjmqfclcaMDe6UaxL+B0Vh4I5mT2zQCJPuGGCZu7PaN00ECgYEA
lGfxDon/GnLSMDmlQY/ZvGA4pEq5go617EP3aoghr8+d73blUhepRmosSoKMkzLl
5atbL3/9l5HMnKX9DfE5A0XHJf9edjckSCezPXB5XNR2byuY5jXbVvzOEENR2gB4
Io6FEYkuBmjDU3LPknrZ5IHM89r2UUeOPhnG8IjKEeECgYArgHuj+aaKhOBPbViR
SuiUbOVs7X2qIGJrUZCkAT+oAxXSym0IFBdjWKWYypy0lrvGXqemJqQzS9os09ns
fbpnQD5fEZLTltpeGbyre6qkyughYa9ukG4MNMiG+UvG9zICARWxe16uGY2U7FZf
egTtF4stEYScwcKW1AAUk+ZLjw==
-----END RSA PRIVATE KEY-----'''


# 签名函数
def sign(params, private_key):
    params = sorted(params.items(), key=lambda e: e[0], reverse=False)
    message = '&'.join(["%s=%s" % (k, v) for k, v in params])
    rsa_key = RSA.importKey(private_key)
    signer = PKCS1_v1_5.new(rsa_key)
    digest = SHA256.new()
    digest.update(message.encode('utf8'))
    sign = signer.sign(digest)
    return base64.b64encode(sign).decode()


# 发送API请求
def alipay_api_request(app_id, method, private_key, params, return_url=None):
    if return_url:
        params.update({'return_url': return_url})
    params.update({
        "app_id": app_id,
        "method": method,
        "format": "JSON",
        "charset": "utf-8",
        "sign_type": "RSA2",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "version": "1.0",
        "biz_content": json.dumps(params)
    })
    params["sign"] = sign(params, private_key)

    print(params)

    print('https://openapi.alipay.com/gateway.do?'+urllib.parse.urlencode(params))
    response = requests.get("https://openapi.alipay.com/gateway.do", params=params)

    # print(response.text)
    # print(response)

    return response


# 创建预支付订单
def create_and_pay(out_trade_no: str, total_amount: float, subject: str='孪生宇宙x普通会员', return_url=None):

    # 创建一个预支付订单
    method = "alipay.trade.page.pay"
    # method = "alipay.trade.precreate"

    params = {
        "out_trade_no": out_trade_no,
        "total_amount": total_amount,
        "subject": subject,
        'product_code': 'FAST_INSTANT_TRADE_PAY'
    }

    # 发送API请求
    params.update({
        'return_url': return_url,
        'notify_url': 'https://api.multicosmo.com/ali/payment',
    })
    params.update({
        "app_id": app_id,
        "method": method,
        "format": "JSON",
        "charset": "utf-8",
        "sign_type": "RSA2",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "version": "1.0",
        "biz_content": json.dumps(params),
    })
    params["sign"] = sign(params, private_key)

    result = 'https://openapi.alipay.com/gateway.do?' + urllib.parse.urlencode(params)

    return result


# 查询订单
def check_trade(out_trade_no: str):
    method = 'alipay.trade.query'
    params = {
        'out_trade_no': out_trade_no,
        # 'trade_no': '',
    }

    r = alipay_api_request(app_id, method, private_key, params)

    logger.info(f"查询 {out_trade_no} 订单返回结果: {r}|{r.text}")
    return r


if __name__ == '__main__':
    r = create_and_pay(str(int(time.time())), 0.01, "测试", 'https://www.multicosmo.com/')
    print(r)
    check_trade('1688435352')

    'https://openapi.alipay.com/gateway.do?out_trade_no=1688435440&total_amount=0.01&subject=%E6%B5%8B%E8%AF%95&product_code=FAST_INSTANT_TRADE_PAY&return_url=https%3A%2F%2Fapi.multicosmo.com%2Fali%2Fpayment&app_id=2021004102603026&method=alipay.trade.page.pay&format=JSON&charset=utf-8&sign_type=RSA2&timestamp=2023-07-04+09%3A50%3A40&version=1.0&biz_content=%7B%22out_trade_no%22%3A+%221688435440%22%2C+%22total_amount%22%3A+0.01%2C+%22subject%22%3A+%22%5Cu6d4b%5Cu8bd5%22%2C+%22product_code%22%3A+%22FAST_INSTANT_TRADE_PAY%22%2C+%22return_url%22%3A+%22https%3A%2F%2Fapi.multicosmo.com%2Fali%2Fpayment%22%7D&sign=eAKuN4Qz7h8wxlutyNg8IqInQuFQPEgNomcmXVbCSueAe6w7C25SoHXEmI7W21kKCdSDHdONqd3uVDntsgRGz%2Br9z9DxUDu%2Bir5XFS%2Bi9dky9sCFSi3udV0Uj3TPMmE6yipHw6uGonluCi1ucKiN4aBsetYto4IGGuGLlXg9eMVyuEpEBh9b5vbcO2uW5NJWBcn0QElrbbqOgcKsSkEqNc%2FEt%2F4hoPsWQnrAFqqlkM13NcqqNFb5UJ%2BPR%2FJ5ZeFeeTd%2B5k2SIawgU042WawargX4O3DOC2Pi7ulgAwez3rzLOWDEi2T8%2BAOvYLL%2FeZOM60zGPtN9fwGVFVpR0UTUWQ%3D%3D'