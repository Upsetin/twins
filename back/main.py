# encoding: utf-8
import datetime
import hashlib
import json
import random
import re

import pymongo
import uvicorn as uvicorn
from fastapi import FastAPI, Response, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse
from pydantic import BaseModel

# stream event
from chat import get_answer
from db import redis_client, mongo_client, MongoClient
from email_api import send_eamil
from encrypt import AES_en, AES_de
from func import make_uuid, xml_to_json, is_educational_email, parse_query_params
from order import create_bill, alipay
from wechat_api import *
from wxpay_api import wx_pay, wxpay_calback

app = FastAPI(docs_url=None)

# 2、声明一个 源 列表；重点：要包含跨域的客户端 源
origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
    # 客户端的源
    # "http://127.0.0.1:5173",
    # "https://127.0.0.1:5173",
    # '*'
]
# 3、配置 CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

'''校验token中间件'''
IGNORE_TOKEN_URL = ['/QrLogin', "/wchat_callback", "/feedback", '/send_code', '/login', '/partnership',
                    '/payment', '/pay', '/wechat/payment', '/ali/payment']  # 添加不需要进行token验证的路径

'''测试'''


@app.get('/pay/{amount}')
def pay(amount: float):
    amount = int(amount * 100)
    out_trade_no = str(int(time.time() * 1000))
    description = '微信支付测试描述'
    r = wx_pay(amount, out_trade_no, description)
    if r['code'] == 200:
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>Base64 Image</title>
</head>
<body>
    <h1>Base64 Image</h1>
<img src="data:image/png;base64,{r['qr_base64']}"/>                                                                                    
</body>
</html>
'''
        return Response(content=html_content, media_type="text/html")
    else:
        return JSONResponse(content=r)


@app.get("/")
async def root():
    return Response(content="What's up man?", media_type="text/html")


# 测试payment
@app.get("/payment")
async def root(count: float = 0.01):
    r = await create_bill(0.01, subject='测试', by_user='test')

    base64_img = r['qr']

    # print(base64_img)
    html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Fullscreen Image Centered</title>
    <style>
        html, body {
            height: 100%;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .image-container {
            max-width: 100%;
            max-height: 100%;
        }

        .image-container img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }
    </style>
</head>
<body>
    <div class="image-container">
        <img src="data:image/jpeg;base64,''' + base64_img + '''" alt="Fullscreen Image">
    </div>
</body>
</html>
'''

    return Response(content=html_content, media_type="text/html")


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get('/wachat_qr')
async def wechat_qr():
    scene_str = str(time.time())
    qr_url = await get_qrcode(scene_str=scene_str)
    html_content = f'''<html style="height: 100%;"><head><meta name="viewport" content="width=device-width, minimum-scale=0.1"><title>showqrcode (430×430)</title></head><body style="margin: 0px; background: #0e0e0e; height: 100%"><img style="display: block;-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 90%);transition: background-color 300ms;" src="{qr_url}"><script src="chrome-extension://idnnbdplmphpflfnlkomgpfbpcgelopg/inpage.js" id="xverse-wallet-provider"></script></body></html>'''
    return Response(content=html_content, media_type="text/html")


'''正式程序'''


@app.middleware('http')
async def judge_token(request: Request, call_next):
    path = request.url.path

    print('path:', path)
    ignore = False
    for i in IGNORE_TOKEN_URL:
        if i in path:
            ignore = True
    if not ignore:
        token = request.headers.get("token")
        print('token:', token)

        try:
            token_str = AES_de(token)
            token_dict = eval(token_str)
            openid = token_dict['openid']
        except:
            res = {'code': 403, "msg": "登录已过期,请重新登录!"}
            return JSONResponse(content=res)

        # Add email to request state for later use
        request.state.openid = openid

    # Continue processing request
    response = await call_next(request)
    return response


'''wechat服务器校验&回调'''
'''/wchat_callback?signature=&echostr=&timestamp=1687859560&nonce=1231493457'''


@app.get("/wchat_callback")
async def verify_wchat_callback(signature: str, timestamp: str, nonce: str, echostr: str):
    token = "LuoYaVxskFceQKH3P5kJHjCYJBh1pB5J"  # 替换为你的微信公众号token

    # 将token、timestamp和nonce按照字典序排序
    sorted_params = sorted([token, timestamp, nonce])

    # 拼接成字符串
    sorted_str = ''.join(sorted_params)

    # 对字符串进行SHA1哈希计算
    sha1 = hashlib.sha1()
    sha1.update(sorted_str.encode('utf-8'))
    hashed_str = sha1.hexdigest()
    print(hashed_str)

    # 比较计算结果与微信发送的signature参数是否一致
    if hashed_str == signature:
        # 验证通过, 返回echostr给微信服务器
        return Response(content=echostr, media_type="text/html")
    else:
        return "Verification failed."


@app.post("/wchat_callback")
async def wchat_callback(request: Request, signature: str = Query(...), nonce: int = Query(...),
                         timestamp: int = Query(...), openid: str = Query(...)):
    raw_data = await request.body()
    # print([raw_data])
    xml_data = ET.fromstring(raw_data)

    # raw-data 转json
    raw_data_json = xml_to_json(raw_data.decode('utf-8'))

    # 解析接收到的消息类型
    msg_type = xml_data.find("MsgType").text
    logger.info(f"收到事件：{msg_type} -> {openid}")
    # print('msg_type:', [msg_type])

    if msg_type == "text":
        # 文本消息

        content = xml_data.find("Content").text

        FromUserName = xml_data.find('FromUserName').text
        ToUserName = xml_data.find('ToUserName').text

        # 根据发送的信息进行回复
        asyncio.create_task(process_answer_message(openid, content))

        # answer = await ask_question(content)

        reply_xml = f'''<xml>
        <ToUserName><![CDATA[{FromUserName}]]></ToUserName>
        <FromUserName><![CDATA[{ToUserName}]]></FromUserName>
        <CreateTime>{int(time.time())}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[正在处理,请稍等...]]></Content>
        </xml>'''
        return Response(content=reply_xml, media_type="application/xml")

    elif msg_type == "event":
        # 事件推送
        event = xml_data.find("Event").text
        FromUserName = xml_data.find('FromUserName').text
        ToUserName = xml_data.find('ToUserName').text
        print('event:', event)

        # if event == "subscribe":
        #     # 用户关注事件
        #     reply_content = "欢迎加入MegaCosmo多元宇宙——迸发想象，创造无限可能"
        #
        #
        #     reply_xml = f'''<xml>
        #     <ToUserName><![CDATA[{FromUserName}]]></ToUserName>
        #     <FromUserName><![CDATA[{ToUserName}]]></FromUserName>
        #     <CreateTime>{int(time.time())}</CreateTime>
        #     <MsgType><![CDATA[text]]></MsgType>
        #     <Content><![CDATA[{reply_content}]]></Content>
        #     </xml>'''
        # reply_xml = generate_text_reply(xml_data, reply_content)

        if event == 'SCAN':
            # 更新qr_code状态
            Ticket = raw_data_json.get('Ticket', None)
            if Ticket:
                filter = {
                    'status': 0,
                    'ticket': Ticket
                }

                updtae = {
                    'status_str': '已使用',
                    'status_code': 1,
                    'update_time': str(datetime.datetime.now())
                }
                MongoClient(collection_name='login_qr_code').update_data(filter, updtae)

                # 查询login_id
                login_id = MongoClient(collection_name='login_qr_code').find({'ticket': Ticket}, only_one=True).get(
                    'login_id')
                # 插入login记录表
                db = {
                    'openid': openid,
                    'datetime': str(datetime.datetime.now()),
                    'ticket': Ticket,
                    'login_id': login_id,
                    'used': 0
                }
                MongoClient(collection_name='login_log').insert_data(db)
                # 查询该openid是否在库中
                query_result = MongoClient(collection_name='user_base_info').find({'openid': openid}, only_one=True)
                #  已存在
                if query_result:
                    user_name = query_result['username']

                    reply_content = f'{user_name}, 欢迎回来~\n\n<a href="https://chat.multicosmo.com">点击返回对话页面</a>'
                # 之前手动关注的，但没注册用户 -> 注册
                else:
                    # 初始化数据
                    username = random.choice(
                        ['Zeus', 'Hera', 'Poseidon', 'Apollo', 'Artemis', 'Aphrodite', 'Hades', 'Hermes', 'Athena',
                         'Hephaestus', 'Ares', 'Dionysus', 'Hestia', 'Maia', 'Persephone', 'Triton', 'Cronus', 'Hera',
                         'Metis', 'Nyx', 'Pallas', 'Titan', 'Hephaeb', 'Semis', 'Coeus', 'Rhea', 'Osiris', 'Satyros',
                         'Demeter', 'Io', 'Themis', 'Lamia', 'Oriana', 'Tantalus', 'Heracles', 'Hermus', 'Phyleus',
                         'Eva', 'Cronus', 'Atlas', 'Theseus', 'Hestia', 'Juno', 'Morden', 'Lina', 'Bios', 'Hermes',
                         'Alex', 'Hephaestus', 'Hefestos', 'Ikaros', 'Titania', 'Cerene', 'Zephyros', 'Icarus',
                         'Kronos', 'Minerva', 'Pitho', 'Ermis', 'Roma', 'Colinus', 'Hestie', 'Ermes', 'Zephyrus',
                         'Ikaros', 'Lina', 'Hefestos', 'Bios', 'Hermes', 'Juno', 'Theseus', 'Heracles', 'Hera',
                         'Poseidon', 'Apollo', 'Artemis', 'Aphrodite', 'Hades', 'Hermes', 'Athena', 'Hephaestus',
                         'Ares', 'Dionysus', 'Hestia', 'Maia', 'Persephone', 'Triton', 'Cronus', 'Hera', 'Metis', 'Nyx',
                         'Pallas', 'Titan', 'Hephaeb', 'Semis', 'Coeus', 'Rhea', 'Osiris', 'Satyros', 'Demeter'])
                    db = {
                        'username': username,
                        'openid': openid,
                        'email': None,
                        'edu_email': None,
                        'is_edu': 0,
                        'create_time': str(datetime.datetime.now()),
                        'update_time': str(datetime.datetime.now()),
                        'user_type': "vip",
                        'user_img': "默认头像",
                        # 'last_login_ip': request.client.host,
                        'last_login_time': str(datetime.datetime.now()),
                        'token': 5000,
                        'vip_start_datetime': None,
                        'vip_start_timestamp': None,
                        'vip_expire_time': None,
                        'type': None
                    }
                    MongoClient(collection_name='user_base_info').insert_data(db)
                    reply_content = f'「{username}」是系统分配的默认用户名,之后可在个人页面里进行修改设置。\n\n公众号已接入GPT,可直接进行对话\n\n官网已支持「连续对话」，可前往官网使用\n\n<a href="https://www.multicosmo.com">点击进入官网</a>\n\n<a href="https://www.multicosmo.com">www.multicosmo.com</a> \n\n祝你遨游畅快~'
            else:
                reply_content = f'欢迎加入MegaCosmo多元宇宙——迸发想象，创造无限可能\n\n公众号已接入GPT,可直接进行对话\n\n官网已支持「连续对话」，可前往官网使用\n\n<a href="https://www.multicosmo.com">点击进入官网</a>\n\n<a href="https://www.multicosmo.com">www.multicosmo.com</a>\n\n依次点击下方菜单「更多->加入AI创作画群」加入专属社群\n\n祝你遨游畅快~'

            reply_xml = f'''<xml>
                        <ToUserName><![CDATA[{FromUserName}]]></ToUserName>
                        <FromUserName><![CDATA[{ToUserName}]]></FromUserName>
                        <CreateTime>{int(time.time())}</CreateTime>
                        <MsgType><![CDATA[text]]></MsgType>
                        <Content><![CDATA[{reply_content}]]></Content>
                        </xml>'''

        # 更新数据库 -> 注册、登录逻辑
        # 关注事件 -> 注册
        # 5min内无重复事件 -> 邮件欢迎注册、介绍
        elif event == 'subscribe':
            Ticket = raw_data_json.get('Ticket', None)
            # 扫码进入
            if Ticket:
                # 查询该openid是否在库中
                query_result = MongoClient(collection_name='user_base_info').find({'openid': openid}, only_one=True)
                #  已存在用户名
                if query_result:
                    user_name = query_result['username']

                    reply_content = f'{user_name}, 欢迎回来~\n\n<a href="https://chat.multicosmo.com">点击返回对话页面</a>'

                else:
                    # 进行注册
                    username = random.choice(
                        ['Zeus', 'Hera', 'Poseidon', 'Apollo', 'Artemis', 'Aphrodite', 'Hades', 'Hermes', 'Athena',
                         'Hephaestus', 'Ares', 'Dionysus', 'Hestia', 'Maia', 'Persephone', 'Triton', 'Cronus', 'Hera',
                         'Metis', 'Nyx', 'Pallas', 'Titan', 'Hephaeb', 'Semis', 'Coeus', 'Rhea', 'Osiris', 'Satyros',
                         'Demeter', 'Io', 'Themis', 'Lamia', 'Oriana', 'Tantalus', 'Heracles', 'Hermus', 'Phyleus',
                         'Eva', 'Cronus', 'Atlas', 'Theseus', 'Hestia', 'Juno', 'Morden', 'Lina', 'Bios', 'Hermes',
                         'Alex', 'Hephaestus', 'Hefestos', 'Ikaros', 'Titania', 'Cerene', 'Zephyros', 'Icarus',
                         'Kronos', 'Minerva', 'Pitho', 'Ermis', 'Roma', 'Colinus', 'Hestie', 'Ermes', 'Zephyrus',
                         'Ikaros', 'Lina', 'Hefestos', 'Bios', 'Hermes', 'Juno', 'Theseus', 'Heracles', 'Hera',
                         'Poseidon', 'Apollo', 'Artemis', 'Aphrodite', 'Hades', 'Hermes', 'Athena', 'Hephaestus',
                         'Ares', 'Dionysus', 'Hestia', 'Maia', 'Persephone', 'Triton', 'Cronus', 'Hera', 'Metis', 'Nyx',
                         'Pallas', 'Titan', 'Hephaeb', 'Semis', 'Coeus', 'Rhea', 'Osiris', 'Satyros', 'Demeter'])
                    db = {
                        'username': username,
                        'openid': openid,
                        'email': None,
                        'edu_email': None,
                        'is_edu': 0,
                        'create_time': str(datetime.datetime.now()),
                        'update_time': str(datetime.datetime.now()),
                        'user_type': "vip",
                        'user_img': "默认头像",
                        # 'last_login_ip': request.client.host,
                        'last_login_time': str(datetime.datetime.now()),
                        'token': 5000,
                        'vip_start_datetime': None,
                        'vip_start_timestamp': None,
                        'vip_expire_time': None,
                        'type': None
                    }
                    MongoClient(collection_name='user_base_info').insert_data(db)

                    reply_content = f'欢迎加入MegaCosmo多元宇宙——迸发想象，创造无限可能\n\n「{username}」是系统分配的默认用户名,可在个人页面里进行修改设置。\n\n公众号已接入GPT,可直接进行对话\n\n官网已支持「连续对话」，可前往官网使用\n\n<a href="https://www.multicosmo.com">点击进入官网</a>\n\n依次点击下方菜单「更多->加入AI创作画群」加入专属社群\n\n<a href="https://www.multicosmo.com">www.multicosmo.com</a> \n\n祝你遨游畅快~'
                reply_xml = f'''<xml>
                            <ToUserName><![CDATA[{FromUserName}]]></ToUserName>
                            <FromUserName><![CDATA[{ToUserName}]]></FromUserName>
                            <CreateTime>{int(time.time())}</CreateTime>
                            <MsgType><![CDATA[text]]></MsgType>
                            <Content><![CDATA[{reply_content}]]></Content>
                            </xml>'''

                # 更新相关数据库
                # 更新qr_code状态
                filter = {
                    'status': 0,
                    'ticket': Ticket
                }

                updtae = {
                    'status_str': '已使用',
                    'status_code': 1,
                    'update_time': str(datetime.datetime.now())
                }
                MongoClient(collection_name='login_qr_code').update_data(filter, updtae)

                # 查询login_id
                login_id = MongoClient(collection_name='login_qr_code').find({'ticket': Ticket}, only_one=True).get(
                    'login_id')
                # 插入login记录表
                db = {
                    'openid': openid,
                    'datetime': str(datetime.datetime.now()),
                    'ticket': Ticket,
                    'login_id': login_id,
                    'used': 0
                }
                MongoClient(collection_name='login_log').insert_data(db)

            # 手动关注
            else:
                reply_content = f'欢迎加入MegaCosmo多元宇宙——迸发想象，创造无限可能\n\n公众号已接入GPT,可直接进行对话\n\n官网已支持「连续对话」，可前往官网使用\n\n<a href="https://www.multicosmo.com">点击进入官网</a>\n\n<a href="https://www.multicosmo.com">www.multicosmo.com</a> \n\n依次点击下方菜单「更多->加入AI创作画群」加入专属社群\n\n祝你遨游畅快~'
                reply_xml = f'''<xml>
                            <ToUserName><![CDATA[{FromUserName}]]></ToUserName>
                            <FromUserName><![CDATA[{ToUserName}]]></FromUserName>
                            <CreateTime>{int(time.time())}</CreateTime>
                            <MsgType><![CDATA[text]]></MsgType>
                            <Content><![CDATA[{reply_content}]]></Content>
                            </xml>'''

        # 取消关注事件 -> 发送邮件、短信——用于反馈
        # 5min内只取消了一下，并不是反复进行关注、取消事件
        elif event == 'unsubscribe':

            reply_content = "有缘再见~"
            reply_xml = f'''<xml>
                        <ToUserName><![CDATA[{FromUserName}]]></ToUserName>
                        <FromUserName><![CDATA[{ToUserName}]]></FromUserName>
                        <CreateTime>{int(time.time())}</CreateTime>
                        <MsgType><![CDATA[text]]></MsgType>
                        <Content><![CDATA[{reply_content}]]></Content>
                        </xml>'''

            db = {
                "event_type": event,
                "timestamp": int(time.time()),
                'datetime': str(datetime.datetime.now()),
                'openid': openid,
            }
            MongoClient(collection_name='event').insert_data(db)
            user_info = MongoClient(collection_name='user_base_info').find({'openid': openid}, only_one=True)

            email_add = user_info['email']
            last_time = MongoClient(collection_name='event').find({'openid': openid})
            last_time = list(last_time)[-1]['timestamp']
            # 再见邮件，引导进行反馈 -> 大于5min
            if email_add and int(time.time()) - last_time > 5 * 60 * 60:
                send_eamil(email_add, '有缘再见~')

        # 回复图片
        elif event == "CLICK":
            reply_xml = f'''<xml>
                        <ToUserName><![CDATA[{FromUserName}]]></ToUserName>
                        <FromUserName><![CDATA[{ToUserName}]]></FromUserName>
                        <CreateTime>{int(time.time())}</CreateTime>
                        <MsgType><![CDATA[image]]></MsgType>
                        <Image>
                            <MediaId><![CDATA[5RvlwM7_SHcY5hNK-bexVpOr69G-Ejatlo9bID8Rc2jwintedfn8S4eLePsBC3yM]]></MediaId>
                        </Image>
                        </xml>'''

            # print('click...')
        else:
            # 其他事件暂不处理
            reply_xml = ""
    else:
        # 其他事件暂不处理
        reply_xml = ""
    # print(reply_xml)
    # 记录交互事件于mongo
    db = {
        'raw_data': raw_data.decode('utf-8'),
        'msg_type': msg_type,
        'reply_xml': reply_xml,
        'datetime': str(datetime.datetime.now()),
        'raw_data_2_json': raw_data_json
    }
    mongo_client['tpcosmo']['event_log'].insert_one(
        db
    )
    logger.debug('已存入数据库 ')

    return Response(content=reply_xml, media_type="application/xml")


# 微信支付回调
@app.post('/wechat/payment')
async def wechat_payment(request: Request):
    headers = request.headers
    body = await request.body()
    body = body.decode()

    try:
        r = wxpay_calback(headers, body)
        # 存入数据库
        '''{'id': '3c4b1734-0eec-51cf-b420-890c849b5c30', 'create_time': '2023-07-03T11:14:25+08:00', 'resource_type': 'encrypt-resource', 'event_type': 'TRANSACTION.SUCCESS', 'summary': '支付成功', 'resource': {'mchid': '1647822871', 'appid': 'wxe59bf8bfee088d72', 'out_trade_no': '1688354040502', 'transaction_id': '4200001860202307032003471962', 'trade_type': 'NATIVE', 'trade_state': 'SUCCESS', 'trade_state_desc': '支付成功', 'bank_type': 'OTHERS', 'attach': '', 'success_time': '2023-07-03T11:14:25+08:00', 'payer': {'openid': 'oB4qP6eXuFoEEz_61EGXlDrR9LlQ'}, 'amount': {'total': 1, 'payer_total': 1, 'currency': 'CNY', 'payer_currency': 'CNY'}}}'''
        MongoClient(collection_name='wxpay_raw_bill').insert_data(r)

        out_trade_no = r["resource"]["out_trade_no"]
        # 校验会员
        # 更新订单数据库
        fix_status = MongoClient(collection_name='create_bill').update_data({'trade_no': out_trade_no},
                                                                            {'update_time': str(
                                                                                datetime.datetime.now()),
                                                                                'status': 1,
                                                                                'status_str': '订单已完成'})
        if fix_status[0]:
            # 查询相关信息
            db = MongoClient(collection_name='create_bill').find({'trade_no': out_trade_no}, only_one=True)
            openid = db['openid']
            # 更新个人数据库
            MongoClient(collection_name='user_base_info').update_data({'openid': openid},
                                                                      {'user_type': db['enrol_type'],
                                                                       'type': db['type'],
                                                                       'vip_start_datetime': str(
                                                                           datetime.datetime.now()),
                                                                       'vip_start_timestamp': int(
                                                                           time.time()),
                                                                       'vip_expire_time': int(
                                                                           time.time()) + 30 * 24 * 60 * 60})
        return Response(content='success')

    except:
        return JSONResponse(content={"code": 500, 'msg': 'erro'})


# 支付宝支付回调
@app.post('/ali/payment')
async def alipay_payment(request: Request):
    headers = request.headers
    body = await request.body()
    body = body.decode()
    body = parse_query_params(body)
    query_params = request.query_params
    print("headers:", headers)
    print("body:", body)
    print("query_params:", query_params)
    # 存入数据库原始内容
    body['note'] = '备注:alipay支付回调原始内容'
    MongoClient(collection_name='alipay_raw_bill').insert_data(
        body
    )
    ''' db = {
            'openid': openid,
            'enrol_type': item.fellow_type,
            'create_time': str(datetime.datetime.now()),
            'platform': item.platform,
            'type': fellow_type,
            'price': price,
            'trade_no': out_trade_no,
            'update_time': str(datetime.datetime.now()),
            'status': 0,  # 0|1|-1
            'pay_id': pay_id,
            'status_str': '已创建订单'  # 已创建订单｜已完成｜订单已超时
        }'''
    if body["trade_status"] == 'TRADE_SUCCESS':
        # 进行会员升级
        out_trade_no = body["out_trade_no"]
        # 更改订单状态
        fix_status = MongoClient(collection_name='create_bill').update_data({'trade_no': out_trade_no},
                                                                            {'update_time': str(
                                                                                datetime.datetime.now()),
                                                                                'status': 1,
                                                                                'status_str': '订单已完成'})
        # 判断是否提前创建订单
        if fix_status[0]:
            # 查询相关信息
            db = MongoClient(collection_name='create_bill').find({'trade_no': out_trade_no}, only_one=True)
            openid = db['openid']
            # 更新个人数据库
            MongoClient(collection_name='user_base_info').update_data({'openid': openid},
                                                                      {'user_type': db['enrol_type'],
                                                                       'type': db['type'],
                                                                       'vip_start_datetime': str(
                                                                           datetime.datetime.now()),
                                                                       'vip_start_timestamp': int(
                                                                           time.time()),
                                                                       'vip_expire_time': int(
                                                                           time.time()) + 30 * 24 * 60 * 60})
            # token 数据更新 「Mongo & Redis」
            pass
        return Response(content='success')
        # 查询订单详情
        # 更改用户会员、token状态
    return Response(content='success', media_type="text/html")


# 支付宝支付回调
@app.get('/ali/payment')
async def alipay_payment(request: Request):
    headers = request.headers
    body = await request.body()
    body = body.decode()
    query_params = request.query_params
    print("headers:", headers)
    print("body:", body)
    print("query_params:", query_params)

    return RedirectResponse(url="https://www.multicosmo.com")


class send_code_en(BaseModel):
    email: str
    event_type: str  # register-注册、forget-忘记密码


'''登陆类'''


# 发送验证码
@app.post('/send_code')
async def send_code(item: send_code_en):
    # 校验邮箱是否合法
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(pattern, item.email):
        return JSONResponse(content={'code': 403, "msg": "邮箱格式有误,请检查后重试!"})

    # 校验是否存在该用户名
    if item.event_type == 'forget':
        if not list(mongo_client['tpcosmo']['user_base_info'].find({'email': item.email})):
            res = {'code': 404, 'msg': f'该邮箱「{item.email}」还未注册!'}
            return JSONResponse(content=res)
    elif item.event_type == 'register':
        if list(mongo_client['tpcosmo']['user_base_info'].find({'email': item.email})):
            res = {'code': 404, 'msg': f'该邮箱「{item.email}」已注册,请登录!'}
            return JSONResponse(content=res)
    else:
        res = {'code': 500, "msg": "不存在该操作!"}
        return JSONResponse(content=res)
    # 检验时效性
    code_create_timestamp = redis_client.hget('verify:code', item.email)
    # print(code_create_timestamp)
    if code_create_timestamp:
        code_create_timestamp = eval(code_create_timestamp.decode())
        # 判断时间是否在限定范围之内
        if int(time.time()) < code_create_timestamp + 60:
            res = {'code': 403, 'msg': f'请{60 - (int(time.time()) - code_create_timestamp)}s后重试...'}
            return JSONResponse(content=res)
    # 生成code
    code = random.randint(1000, 9999)
    # print("code:", code)
    # 发送验证码
    pass
    # 存入数据库
    db = {
        'email': item.email,
        'code': code,
        'create_time': str(datetime.datetime.now()),
        'expire_time': int(time.time()) + 60,
        'is_ok': 1,
        'event_type': item.event_type
    }
    mongo_client['tpcosmo']['verify_code'].insert_one(
        db
    )
    # 存入redis
    redis_client.hset('verify:code', item.email, int(time.time()))
    res = {'code': 200, 'msg': 'success'}
    return res


'''用户类'''


@app.post('/QrLogin')
async def QrLogin():
    # 自我生成uuid
    login_id = make_uuid()

    # 二维码参数值
    scene_str = str(time.time())
    # 扫描二维码
    qr_url, ticket = await get_qrcode()

    # 存入数据库
    db = {
        "qr_url": qr_url,
        "date_time": str(datetime.datetime.now()),
        "login_id": login_id,
        "scene_str": scene_str,
        "status_str": "已创建",
        "status_code": 0,
        'update_time': str(datetime.datetime.now()),
        'ticket': ticket
    }

    MongoClient(collection_name='login_qr_code').insert_data(db)

    # 返回数据
    r_db = {
        "code": 200,
        'qr_url': qr_url,
        "msg": "success",
        "login_id": login_id
    }
    return JSONResponse(content=r_db)


# 查询扫码情况
@app.get("/QrLogin/{login_id}")
async def check_login(login_id: str):
    # 记录登录情况
    # 在redis中检测是否有该用户信息，若没有加入用户表，同时更新login_log，否则只更新login_log
    r = MongoClient(collection_name='login_log').find({'login_id': login_id, 'used': 0}, only_one=True)
    # 扫描成功
    if r:
        openid = r['openid']
        data = {'random_str': ''.join(
            random.choices('qwertyasklzxcvbnm1237890QWERTYUIOPASDFGHJKLZXCVBNM', k=random.randint(1, 10))),
            'openid': openid, 'data_time': str(datetime.datetime.now())}
        # 生成token
        token = AES_en(str(data))

        r = {
            "code": 200,
            "msg": "success",
            "token": token
        }

        # 更新数据库
        filter = {'openid': openid}
        update = {
            'used': 1
        }
        MongoClient(collection_name='login_log').update_data(filter, update)

        # 更新user表
        filter = {'openid': openid}
        update = {'last_login_time': str(datetime.datetime.now())}
        MongoClient(collection_name='user_base_info').update_data(filter, update)

        return JSONResponse(content=r)

    # 不存在
    if not r:
        r = {
            'code': 404,
            'msg': '不存在该login_id',
        }
        return JSONResponse(content=r)

    # 等待扫描
    r = {
        'code': 201,
        'msg': 'wait scan...',
    }
    return JSONResponse(content=r)


# 获取个人信息
@app.get("/user_data")
async def check_login(request: Request):
    openid = request.state.openid if hasattr(request.state, "openid") else None

    # print('email:', email)

    # 查询用户信息
    r = MongoClient(collection_name='user_base_info').find({'openid': openid}, only_one=True)
    if r:
        data = {
            'username': r['username'],
            # 'email': r['email'],
            'user_type': r['user_type'],
            'user_img': r['user_img'],
            'is_edu': r['is_edu']
        }
    else:
        res = {'code': 500, 'msg': "登录过期,请重新登录"}
        return JSONResponse(content=res)
    # 提取信息
    r = {
        "code": 200,
        "msg": "success",
        "data": data
    }
    return JSONResponse(content=r)


'''订单类'''


# 生成支付二维码
class enrol_type(BaseModel):
    fellow_type: str
    platform: str  # wechat|alipay


@app.post("/enrol")
async def enrol(request: Request, item: enrol_type):
    openid = request.state.openid if hasattr(request.state, "openid") else None

    print(openid)
    print(item)
    price_board = {
        "VIP": 35,
        "edu_VIP": 35,
        "Professional": 168
    }

    price = price_board.get(item.fellow_type, None)

    if item.platform not in ['alipay', 'wechat', 'wechat1']:
        return {"code": 403, "msg": "请重新选择支付方式!"}

    if not price:
        r = {"code": 403, "msg": "不存在该会员类型"}
        return JSONResponse(status_code=500, content=r)

    pay_id = make_uuid()

    # 支付宝
    if item.platform == 'alipay':
        # 生成订单信息
        qr_res, out_trade_no = await alipay(price, 'TwinParticle' + item.fellow_type, openid)
        # print(qr_res)
        # 预创建订单
        if item.fellow_type == 'edu_VIP':
            fellow_type = '教育优惠'
            # 校验 教育认证
            if not MongoClient(collection_name='user_base_info').find({'openid': openid, 'is_edu': 1}):
                return JSONResponse(content={'code': 403, 'msg': "请完成教育认证后重试!"})
        elif item.fellow_type == 'VIP':
            fellow_type = '标准会员'
        else:
            fellow_type = '专业会员'
        # 存入数据库
        db = {
            'openid': openid,
            'enrol_type': item.fellow_type,
            'create_time': str(datetime.datetime.now()),
            'platform': item.platform,
            'type': fellow_type,
            'price': price,
            'trade_no': out_trade_no,
            'update_time': str(datetime.datetime.now()),
            'status': 0,  # 0|1|-1
            'pay_id': pay_id,
            'status_str': '已创建订单'  # 已创建订单｜已完成｜订单已超时
        }
        MongoClient(collection_name='create_bill').insert_data(db)
        # 无需处理，其函数已处理
        return JSONResponse(content=qr_res)
    # 微信
    elif item.platform == 'wechat':
        if item.fellow_type == 'edu_VIP':
            fellow_type = '教育优惠'
            # 校验 教育认证
            if not MongoClient(collection_name='user_base_info').find({'openid': openid, 'is_edu': 1}):
                return JSONResponse(content={'code': 403, 'msg': "请完成教育认证后重试!"})
        elif item.fellow_type == 'VIP':
            fellow_type = '标准会员'
        else:
            fellow_type = '专业会员'

        amount = int(price * 100)
        description = fellow_type
        out_trade_no = str(int(time.time() * 1000))
        qr_base64 = wx_pay(amount, out_trade_no, description)

        # 存入数据库
        db = {
            'openid': openid,
            'enrol_type': item.fellow_type,
            'create_time': str(datetime.datetime.now()),
            'platform': item.platform,
            'type': fellow_type,
            'price': price,
            'trade_no': out_trade_no,
            'update_time': str(datetime.datetime.now()),
            'status': 0,  # 0|1|-1
            'pay_id': pay_id,
            'status_str': '已创建订单'  # 已创建订单｜已完成｜订单已超时
        }

        MongoClient(collection_name='create_bill').insert_data(db)

        respond = {
            "code": 200,
            "pay_qr": qr_base64['qr_base64'],
            "msg": "success",
            'pay_id': pay_id,
            "total_amount": price,
        }
        return JSONResponse(content=respond)
    elif item.platform == 'wechat1':
        print(f'捕获到请求: {item}')
        if item.fellow_type == 'edu_VIP':
            fellow_type = '教育优惠'
            # 校验 教育认证
            if not MongoClient(collection_name='user_base_info').find({'openid': openid, 'is_edu': 1}):
                return JSONResponse(content={'code': 403, 'msg': "请完成教育认证后重试!"})
        elif item.fellow_type == 'VIP':
            fellow_type = '标准会员'
        else:
            fellow_type = '专业会员'

        amount = int(price * 100)
        description = fellow_type
        out_trade_no = str(int(time.time() * 1000))
        print("amount:", amount)
        result = wx_pay(amount, out_trade_no, description, 'JSAPI', openid)

        # 存入数据库
        db = {
            'openid': openid,
            'enrol_type': item.fellow_type,
            'create_time': str(datetime.datetime.now()),
            'platform': item.platform,
            'type': fellow_type,
            'price': price,
            'trade_no': out_trade_no,
            'update_time': str(datetime.datetime.now()),
            'status': 0,  # 0|1|-1
            'pay_id': pay_id,
            'status_str': '已创建订单'  # 已创建订单｜已完成｜订单已超时
        }

        MongoClient(collection_name='create_bill').insert_data(db)

        respond = result
        print(respond)
        return JSONResponse(content=respond)

    else:
        return JSONResponse(status_code=403, content={'code': 403, 'msg': '请重新选择支付方式!'})


# 查询支付情况
@app.get("/check_pay/{pay_id}")
async def check_pay(request: Request, pay_id: str):
    openid = request.state.openid if hasattr(request.state, "openid") else None

    # 查询数据库
    r = MongoClient(collection_name='create_bill').find({'openid': openid, 'pay_id': pay_id}, only_one=True)
    if r:
        if r['status'] == 1:
            respond = {
                "code": 200,
                "msg": "success",
            }
        else:
            respond = {
                "code": 201,
                "msg": "waiting~",
            }
    else:
        respond = {
            "code": 404,
            "msg": "不存在该订单号！",
        }

    return JSONResponse(content=respond)


# 查询历史订单
@app.post('/bill')
async def get_bill():
    r = {
        "code": 200,
        "msg": "success",
        "data": [
            {
                "update_time": "完成时间",
                "create_time": "创建时间",
                "type": "会员类型",
                "total_amount": "总金额"
            },
            {
                "update_time": "完成时间",
                "create_time": "创建时间",
                "type": "会员类型",
                "total_amount": "总金额"
            },
            {
                "update_time": "完成时间",
                "create_time": "创建时间",
                "type": "会员类型",
                "total_amount": "总金额"
            }
        ]
    }
    return JSONResponse(content=r)


'''聊天类'''


# 获取新的chat_id,用于开启会话
@app.post('/get_chat_id')
async def get_chat_id(request: Request):
    openid = request.state.openid if hasattr(request.state, "openid") else None

    while True:

        chat_id = make_uuid()

        # 判断是否存在该chat_id
        # 先查询redis
        '''【hash】【chat:chat_id】【32303233-2D30362D-31312031-373A3535-3A32382E-32373038-3938】【test@gmail.com】 '''
        if redis_client.hget('chat:chat_id', chat_id):
            # 存在该uuid
            continue
        # 再查询mongo -> mongodb中存在该chat_id
        if not mongo_client['tpcosmo']['chat_id'].find({'chat_id': chat_id}):
            continue
        break

    # 插入redis、mongodb
    redis_client.hset('chat:chat_id', chat_id, openid)
    # 插入mongodb
    mongo_client['tpcosmo']['chat_id'].insert_one(
        {
            'chat_id': chat_id,
            'by_user': openid,
            'create_time': str(datetime.datetime.now()),
            # 是否使用
            'is_use': 0,
            # 用于展示在侧边历史栏
            'title': 'New Chat',
            # 是否被用户删除
            'del': 0,
            # 更新时间
            'update_time': str(datetime.datetime.now())
        }
    )
    logger.info(f'char_id: {chat_id}|已插入数据库')
    r = {
        "code": 200,
        "msg": "success",
        "chat_id": chat_id
    }

    return JSONResponse(content=r)


class chat_en(BaseModel):
    content: str
    chat_id: str


class chat_content(BaseModel):
    content: str
    chat_id: None | str


def extract_text(input_string):
    # 匹配中文字符
    chinese_pattern = r'[\u4e00-\u9fff]+'

    # 匹配英文单词
    english_pattern = r'\b\w+\b'

    # 查找所有中文字符
    chinese_matches = re.findall(chinese_pattern, input_string)

    # 查找所有英文单词
    english_matches = re.findall(english_pattern, input_string)

    if chinese_matches:
        # 取前5个中文字符或所有中文字符（取最小值）
        result = "".join(chinese_matches[:5])
    elif english_matches:
        # 取前5个英文单词或所有英文单词（取最小值）
        result = " ".join(english_matches[:5])
    else:
        # 若没有中文字符和英文单词，则取前10个字符
        result = input_string[:10]

    return result


@app.post('/chat')
async def chat(request: Request, item: chat_en):
    # 提取user_id，即email
    openid = request.state.openid if hasattr(request.state, "openid") else None

    # 获取token
    base_info = MongoClient(collection_name='user_base_info').find({'openid': openid}, only_one=True)
    if base_info['token'] <= 0 and base_info['user_type'] == 'vip':
        return Response(content="试用额度已使用完，请订阅会员后重试~\n\n教育优惠仅需¥35,快去认证吧!",
                        media_type="text/html")
    # 在redis中查询该对话
    if not redis_client.hget('chat:chat_id', item.chat_id):
        # 存在该对话id，立马删除，以免出现堆积or误会
        # redis_client.srem('chat:chat_id', item.chat_id)
        # return {'code': 404, 'msg': "不存在该对话"}
        return Response(content='data: [ERRO] 不存在该对话...', media_type="text/html")

    # 更改chat_id状况
    filter = {
        'is_use': 0,
        'chat_id': item.chat_id,
        'by_user': openid,
    }

    updtae = {
        'is_use': 1,
        'title': extract_text(item.content),
        'update_time': str(datetime.datetime.now())
    }
    MongoClient(collection_name='chat_id').update_data(filter, updtae)  # 实现每次只能回答一个问题
    # 0 -> 当前正在生成回答, 不可生成回答
    # 1 -> 当前可回答
    t = redis_client.hget('chat:lock_one_time', openid)
    if not t:
        redis_client.hset('chat:lock_one_time', openid, 1)

    # print('t:', type(t), t)
    # if redis_client.hget('chat:lock_one_time', openid).decode() == '0':
    #     return Response(content='data: [ERRO] 同一时间只能生成一个回答,请重试...', media_type="text/html")

    # 上锁，不允许同时多个回答
    redis_client.hset('chat:lock_one_time', openid, 0)

    prompt = item.content
    # print('prompt:', prompt)

    # 暂不处理
    accept = request.headers.get("Accept")
    user_agent = request.headers.get("User-Agent")

    # 处理请求...
    # return StreamingResponse(get_answer(item, prompt, by_user=openid), media_type="text/event-stream")

    # 实现连续对话
    # 查询数据库对话内容
    # {
    #     # "_id": ObjectId("64b8effdd6c9b7af31bdbfa8"),
    #     "chat_id": "32303233-2D30372D-32302031-363A3231-3A33362E-38373630-3233",
    #     "user_content": "怎么样将Pigm基因映射到GM4 BAC连锁图中的一个特定区间来确定其位置",
    #     "got_content": "要将Pigm基因映射到GM4 BAC连锁图中的特定区间来确定其位置，可以采取以下步骤：\n\n1. 获取Pigm基因的序列信息，并与GM4 BAC连锁图中已知的标记物或基因进行比对。这可以通过基因组测序和比对工具（如BLAST）来完成。\n\n2. 确定Pigm基因与GM4 BAC连锁图中的标记物或基因的关联性。这可以通过查阅相关文献或数据库，如NCBI或Ensembl进行比对和分析。\n\n3. 根据关联性，确定Pigm基因在GM4 BAC连锁图中的大致位置。这可以通过比对结果的位置信息和连锁图的已知信息来推断。\n\n4. 确定Pigm基因在GM4 BAC连锁图中的确切位置，可以通过进一步实验验证和验证。例如，可以使用引物扩增和测序技术，对GM4 BAC连锁图中的相关区域进行特异性扩增和测序。\n\n以上是一般的步骤，具体的实施方法可能因具体情况而异。建议在进行实验之前，仔细研究相关文献和数据库，以确定正确的实验设计和方法。",
    #     "create_time": "2023-07-20 16:27:41.810121",
    #     "gpt_type": "gpt-3.5-turbo-0613",
    #     "by_user": "oB4qP6W8kQzYdncDpsnXnNhCRieY",
    #     "total_cost_time": "null",
    #     # "total_tokens": NumberInt(414)
    # }

    chat_history = mongo_client['tpcosmo']['chat_log'].find({'by_user': openid, 'chat_id': item.chat_id}).sort("_id",
                                                                                                               pymongo.DESCENDING).limit(
        3)

    all_question = []
    for i in chat_history:
        logger.info('查询聊天历史:', i)
        # 只添加user问题内容
        all_question.append({"role": "user", "content": i['user_content']}, )

    # 添加当前问题
    all_question.append({"role": "user", "content": prompt}, )

    response = ask_question_raw_data(all_question)

    respond_content = response["choices"][0]["message"]["content"]
    total_tokens = response["usage"]["total_tokens"]

    # 将回答存入对话数据库
    mongo_client['tpcosmo']['chat_log'].insert_one(
        {
            'chat_id': item.chat_id,
            'user_content': item.content,
            'got_content': respond_content,
            'create_time': str(datetime.datetime.now()),
            'gpt_type': response["model"],
            'by_user': openid,
            'total_cost_time': 'null',
            'total_tokens': total_tokens
        }
    )
    print(f"Full conversation received: {respond_content}")
    redis_client.hset('chat:lock_one_time', openid, 1)

    # 更新token消耗
    filter = {
        'openid': openid
    }
    update_data = {
        'token': base_info['token'] - total_tokens
    }
    MongoClient(collection_name='user_base_info').update_data(
        filter, update_data
    )
    return Response(content=respond_content, media_type="text/html")


@app.post('/chat_stream')
async def chat(request: Request, item: chat_content):
    print('item:', item)
    # 提取user_id，即email
    openid = request.state.openid if hasattr(request.state, "openid") else None

    # 获取token
    base_info = MongoClient(collection_name='user_base_info').find({'openid': openid}, only_one=True)
    if base_info['token'] <= 0 and base_info['user_type'] == 'vip':
        return Response(content="试用额度已使用完，请订阅会员后重试~\n\n限时优惠🔥仅需¥35!",
                        media_type="text/html")

    # 不携带chat_id
    if not item.chat_id:
        is_new_chat = True
        item.chat_id = make_uuid()

    # 携带id说明肯定库里有
    else:
        is_new_chat = False

        query = {
            'by_user': openid,
            'chat_id': item.chat_id,
            'del': 0
        }
        r = MongoClient(collection_name='chat_id').find(query, only_one=True)
        if not r:
            return Response(content='erro: 不存在该对话~')

    # 0 -> 当前正在生成回答, 不可生成回答
    # 1 -> 当前可回答
    t = redis_client.hget('chat:lock_one_time', openid)
    if not t:
        redis_client.hset('chat:lock_one_time', openid, json.dumps({'t': int(time.time()), 'is_ok': 1}))
    # else:
    #     print('t:', type(t), t)
    #     t = json.loads(t)
    #     if t['is_ok'] == 0:
    #         if int(time.time()) - t['t'] >= 30:
    #             redis_client.hset('chat:lock_one_time', openid, json.dumps({'t': int(time.time()), 'is_ok': 1}))
    #         else:
    #             return Response(content='<p style="color: darkred;">erro:同一时间只能生成一个回答,请重试...</p>', media_type="text/html")

    # 上锁，不允许同时多个回答
    # redis_client.hset('chat:lock_one_time', openid, json.dumps({'t': int(time.time()), 'is_ok': 0}))

    prompt = item.content

    # 暂不处理
    accept = request.headers.get("Accept")
    user_agent = request.headers.get("User-Agent")

    # 传入待入库参数
    db = {
        "chat_id": item.chat_id,
        "by_user": openid,
        "create_time": str(datetime.datetime.now()),
        "is_use": 1,
        "title": extract_text(item.content),
        "del": 0,
        "update_time": str(datetime.datetime.now())
    }

    all_question = [{'role': 'system',
                     'content': "Answer questions as friendly and detailed as possible. If there are no special requirements, please answer in Chinese"}, ]

    # 查询历史记录
    if not is_new_chat:
        chat_history = mongo_client['tpcosmo']['chat_log'].find({'by_user': openid, 'chat_id': item.chat_id}).sort(
            "_id",
            pymongo.DESCENDING).limit(
            3)
        for i in chat_history:
            logger.info(f'查询聊天历史: {i}')
            # 只添加user问题内容
            all_question.append({"role": "user", "content": i['user_content']}, )
            all_question.append({"role": "assistant", "content": i["got_content"]})

    # 添加当前问题
    all_question.append({"role": "user", "content": prompt})

    return StreamingResponse(get_answer(item, all_question, by_user=openid, is_new_chat=is_new_chat, db=db),
                             media_type="text/event-stream")


# 获取聊天历史
class chat_list_en(BaseModel):
    page: int
    page_size: int


@app.post('/chat_list')
async def get_chat_list(request: Request, item: chat_list_en):
    openid = request.state.openid if hasattr(request.state, "openid") else None

    # 记得判断page_size的上限大小
    if item.page_size >= 20:
        item.page_size = 20

    if item.page < 0:
        item.page = 1

    # 查询记录
    r = mongo_client['tpcosmo']['chat_id'].aggregate(
        [
            {
                '$match': {
                    'by_user': openid,
                    'is_use': 1,
                    'del': 0
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'chat_id': 1,
                    'create_time': 1,
                    'title': 1
                }
            },
            {
                '$skip': (item.page - 1) * 20
            },
            {
                '$limit': item.page_size
            },
        ]
    )

    r = list(r)
    logger.info(f"查询chat_id_list: {len(r)}条")
    r = {
        "code": 200,
        "msg": "success",
        "data": r
    }
    return JSONResponse(content=r)


class clean_item(BaseModel):
    data: list | None


@app.post('/clean')
async def clean(request: Request, item: clean_item):
    openid = request.state.openid if hasattr(request.state, "openid") else None
    if item.data:
        for chat_id in item.data:
            filter = {
                'del': 0,
                'chat_id': chat_id,
                'by_user': openid
            }
            updtae = {
                'del': 1,
                'update_time': str(datetime.datetime.now())
            }
            MongoClient(collection_name='chat_id').update_data(filter, updtae)
    else:
        filter = {
            'del': 0,
            'by_user': openid
        }
        updtae = {
            'del': 1,
            'update_time': str(datetime.datetime.now())
        }
        MongoClient(collection_name='chat_id').update_data(filter, updtae, update_many=True)

    return JSONResponse(content={'code': 200, 'msg': 'success'})


class chat_content(BaseModel):
    chat_id: str
    page_size: int
    page: int


@app.post('/chat_content')
async def get_chat_content(request: Request, item: chat_content):
    openid = request.state.openid if hasattr(request.state, "openid") else None
    # print('email:', email)

    if item.page_size > 10:
        item.page_size = 10

    if item.page < 0:
        item.page = 1

    # print('page_size:', item.page_size)
    # 查询数据库具体内容

    start_time = time.time()
    pipeline = [
        # 筛选条件
        {"$match": {"by_user": openid, 'chat_id': item.chat_id}},
        # 排序
        # {"$sort": {"create_time": -1}},
        {'$project': {'_id': 0, 'user': '$user_content', 'assitant': '$got_content'}},
        # 跳过前 10 条数据
        {"$skip": (item.page - 1) * item.page_size},
        # 限制返回的结果数量为 10 条
        {"$limit": item.page_size}
    ]

    data = mongo_client['tpcosmo']['chat_log'].aggregate(pipeline)
    data = list(data)

    # print('cost_time:', time.time()-start_time)
    # print('data:', data)

    r = {
        "code": 200,
        "msg": "success",
        "data": data
    }
    return JSONResponse(content=r)


'''教育认证'''


# 教育认证发送验证码
class auth_email(BaseModel):
    email: str


@app.post('/edu_code')
async def get_edu_code(request: Request, item: auth_email):
    openid = request.state.openid if hasattr(request.state, "openid") else None

    # 检查邮箱是否符合标准
    if is_educational_email(item.email):
        # 先检查，redis中有没有该邮箱，若有，计算超时时间返回
        r = MongoClient(collection_name='verify_code').find({'openid': openid, 'email': item.email}, only_one=True,
                                                            is_last=True)
        if r and int(time.time()) < r['send_timestamp'] + 60:
            return_data = {
                "code": 403,
                "msg": f"请求验证码频繁, {60 - (int(time.time()) - r['send_timestamp'])}s后重试",
            }
            return JSONResponse(content=return_data)

        random_code = random.randint(1000, 9999)
        email_content = f'您正在进行TwinParticle教育认证\n\n验证码是{random_code},5分钟内有效'
        if send_eamil(item.email, email_content):
            # 更新mongo记录
            db = {
                'openid': openid,
                'email': item.email,
                'code': random_code,
                'create_time': str(datetime.datetime.now()),
                'send_timestamp': int(time.time()),
                'expire_time': int(time.time()) + 5 * 60,
                'used': 0,
                'event_type': 'edu_auth',
                'update_time': str(datetime.datetime.now())
            }
            MongoClient(collection_name='verify_code').insert_data(db)
            r = {
                "code": 200,
                "msg": "success",
            }
            return JSONResponse(content=r)
        else:
            # 若没有直接发送邮件，再写入mongo数据库
            r = {
                "code": 500,
                "msg": "发送失败!",
            }
            return JSONResponse(content=r)
    else:
        r = {
            'code': 403,
            'msg': f'「{item.email}」非教育邮箱!\n若有误请反馈至「help@multicosmo.com」'
        }
        return JSONResponse(content=r)


# 教育认证
class edu_entity(BaseModel):
    email: str
    code: int


@app.post('/edu_auth')
# 教育邮箱认证
async def edu_auth(request: Request, item: edu_entity):
    openid = request.state.openid if hasattr(request.state, "openid") else None
    # 查询验证码记录
    email_code_query = MongoClient(collection_name='verify_code').find(
        {'openid': openid, 'email': item.email, 'used': 0}, only_one=False)
    print(email_code_query)
    # 循环检查是否已过期，如果有，则修改状态
    for i in email_code_query:
        if int(time.time()) > i['expire_time']:
            # 更新验证码状态
            MongoClient(collection_name='verify_code').update_data({'_id': i['_id']}, {'used': -1})
    # 再次查询验证码
    email_code_query = MongoClient(collection_name='verify_code').find(
        {'openid': openid, 'email': item.email, 'used': 0}, only_one=False)
    if email_code_query:
        email_code_query = email_code_query[-1]

        if int(time.time()) > email_code_query['expire_time']:
            # 过期
            r = {
                "code": 403,
                "msg": "验证码已过期!",
            }
            # 更新数据库
            filter = {'openid': openid, 'email': item.email, 'used': 0}
            update = {'used': 1, 'update_time': str(datetime.datetime.now())}
            MongoClient(collection_name='verify_code').update_data(filter, update)
            return JSONResponse(content=r)
        elif email_code_query['code'] != item.code:
            # erro
            r = {
                "code": 403,
                "msg": "验证码错误!",
            }
            return JSONResponse(content=r)
        #  email_code_query['code'] == item.code
        else:
            # 更新验证码数据库
            filter = {'email': item.email, 'used': 0, 'code': item.code, 'openid': openid}
            update = {'used': 1, 'update_time': str(datetime.datetime.now())}
            MongoClient(collection_name='verify_code').update_data(filter, update)

            # 更新个人信息
            filter = {'openid': openid}
            update = {'is_edu': 1, 'edu_email': item.email}
            MongoClient(collection_name='user_base_info').update_data(filter, update)
            # 认证成功
            r = {
                "code": 200,
                "msg": "认证成功!",
            }
            return JSONResponse(content=r)
    else:
        r = {
            "code": 404,
            "msg": "请先发送验证码至邮箱!",
        }
        return JSONResponse(content=r)


'''反馈&商务合作'''


# 反馈
class fb_en(BaseModel):
    content: str
    contact: str


@app.post('/feedback')
async def feedback(item: fb_en):
    item = item.dict()
    item['create_time'] = str(datetime.datetime.now())

    MongoClient(collection_name='feedback').insert_data(item)

    r = {
        "code": 200,
        "msg": "感谢反馈，我们会尽快给你回复!"
    }

    return JSONResponse(content=r)


# 商务合作
class partner_en(BaseModel):
    contact: str
    note: str


@app.post('/partnership')
async def partnership(item: partner_en):
    item = item.dict()
    item['create_time'] = str(datetime.datetime.now())
    MongoClient(collection_name='partnership').insert_data(
        item
    )

    r = {
        "code": 200,
        "msg": "我们已收到你的合作意愿，期待合作愉快!",
    }

    return JSONResponse(content=r)


if __name__ == '__main__':
    uvicorn.run(app="main:app", host='0.0.0.0', port=8008, workers=16)
