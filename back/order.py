import asyncio
import datetime
import time

from loguru import logger
from fastapi.responses import JSONResponse

from alipay_func import create_and_pay, check_trade
from db import mongo_client, redis_client, MongoClient
from func import make_qr_img, make_uuid


# 创建阿里订单
async def alipay(total_amount: float, subject: str, by_user: str):
    '''

    :param total_amount: 总金额
    :param subject: 备注
    :return: 创建结果
    '''

    # 预创建订单
    out_trade_no = make_uuid()
    pay_url = create_and_pay(out_trade_no, total_amount=total_amount, subject=subject, return_url='https://chat.multicosmo.com/')

    # 定价表
    price_board = {
        68: "标准会员",
        35: "教育优惠/标准会员",
        168: "高级会员"
    }

    subscribe_type = price_board.get(total_amount, None)

    db = {
        'create_time': str(datetime.datetime.now()),
        'user_id': by_user,
        'update_time': str(datetime.datetime.now()),
        'total_amount': total_amount,
        'type': subscribe_type,
        # 'status': '等待扫码',
        # 判断是否有效
        # 'is_live': 1,
        'trade_no': '',
        'pay_url': pay_url,
        'out_trade_no': out_trade_no
    }
    # 数据库
    MongoClient("ali_pc_pay").insert_data(db)

    res = {
        "code": 200,
        "pay_url": pay_url
    }
    return res, out_trade_no


# 创建订单
async def create_bill(total_amount: float, subject: str, by_user: str):
    '''

    :param total_amount: 总金额
    :param subject: 备注
    :return: 创建结果
    '''

    # 预创建订单
    out_trade_no = make_uuid()
    r = create_and_pay(out_trade_no, total_amount=total_amount, subject=subject)
    print('r:', r)
    '''{'alipay_trade_precreate_response': {'code': '10000', 'msg': 'Success', 'out_trade_no': 'test000003', 'qr_code': 'https://qr.alipay.com/bax04616fwkp7py9gcsn2528'}, 'sign': 'u3UzFESDZHohfKlh1IM4jKEo7HEb7pttyHrsxMDu3sUe9P9KhUzFry4ecU5Qsbrp1xrPlQ1L3D6lGqrX94kkUPeRStlVtvjVIVoXcrJ3yY2VAVTHB2JMIOn2d+TcjMu9559h6f28uXW4L0M8TTqUe5lC4xHiWXRy7fpdafZwN9s9O8LNMaeep2e8lciYeh+iAuraPWXcs6PrC2YFRUiMda/p62PDmFcluzXe7uH8jOCxu0k5mo9H+plFxEYBDem5FATBzjfbgRssafAPKzbwOKH1vUjJpFysZlvPi7AETmAP9Cqtp1mMDkhNW/1+DFXG35CzWGDsZvyh1QHM5C5+Kg=='}'''
    if r['alipay_trade_precreate_response']['code'] != '10000':
        # 发送预警通知
        return {"code": 500, "msg": r['alipay_trade_precreate_response']['msg']}

    qr_code = r['alipay_trade_precreate_response']['qr_code']
    out_trade_no = r['alipay_trade_precreate_response']['out_trade_no']

    qr_base64 = make_qr_img(qr_code)

    # 定价表
    price_board = {
        68: "标准会员",
        35: "教育优惠/标准会员",
        168: "高级会员"
    }

    subscribe_type = price_board.get(total_amount, None)

    db = {
        'create_time': str(datetime.datetime.now()),
        'user_id': by_user,
        'update_time': str(datetime.datetime.now()),
        'total_amount': total_amount,
        'type': subscribe_type,
        'status': '等待扫码',
        # 判断是否有效
        # 'is_live': 1,
        'trade_no': '',
        'qr_code': qr_code,
        'out_trade_no': out_trade_no
    }
    # 数据库
    mongo_client['tpcosmo']['create_bill'].insert_one(
        db
    )

    res = {
        "code": 200,
        "qr": qr_base64,
        "msg": "success",
        "pay_id": out_trade_no,
        "total-amount": total_amount
    }
    return res



# 查询订单
async def check_bill(out_trade_no: str):
    r = check_trade(out_trade_no)
    '''
    {'alipay_trade_query_response': {'msg': 'Business Failed', 'code': '40004', 'out_trade_no': 'xxx', 'sub_msg': '交易不存在', 'sub_code': 'ACQ.TRADE_NOT_EXIST', 'receipt_amount': '0.00', 'point_amount': '0.00', 'buyer_pay_amount': '0.00', 'invoice_amount': '0.00'}, 'sign': 'tJmENXGlBqMhdjXCJyuHBbW8F5WY5GfSF5H6OsjqaWRlEPuAb6dUYAdF/2MALpiYl3rF2vzlpMpQ2471yZNc69NHQ/A8/a6OIThf4YWitmJX3KnUGjg2UvtcfQf057m5lSoDul/HovN0hJwphd5waG60Z2n75BTvIby7tE3hQSmOwFGgbvV/fdFykvXtQOFbb+jS1g8wyInv2DbwbRYxjIooi1V2sHdD5ACFLijmDM/L7p9Vbd0Ej2o8VP568aRtGhGzD4c6CyxrRBY/h7M34YfPfWanhW96OMbkTeZd8Kpy1WK42ibt6tgwvppPI4oa7qzHcBl+Hc3/Yn1eD2Y3/w=='}
    '''
    # 交易不存在 ———— 未扫码
    if r['alipay_trade_query_response']['code'] != '10000':
        r = {
            "code": 404,
            "msg": "待扫码~",
        }

        return r

    # 等待付款
    elif r["alipay_trade_query_response"]["trade_status"] == 'WAIT_BUYER_PAY':
        db = r['alipay_trade_query_response']
        # 更新交易数据库
        trade_no = r["alipay_trade_query_response"]["trade_no"]
        filter = {
            'trade_no': trade_no
        }
        mongo_client['tpcosmo']['bill'].update_one(
            filter,
            {'$set': {'update_time': str(datetime.datetime.now()), **db}},
            upsert=True
        )
        logger.debug(f"已更新「bill」数据库: {db}")

        # 更新预创建付款数据库
        out_trade_no = r["alipay_trade_query_response"]["out_trade_no"]
        filter = {
            'out_trade_no': out_trade_no
        }
        db = {
            'update_time': str(datetime.datetime.now()),
            'status': '等待付款',
            'trade_no': trade_no,
        }
        mongo_client['tpcosmo']['create_bill'].update_one(
            filter,
            {'$set': {'update_time': str(datetime.datetime.now()), **db}},
            upsert=True
        )
        logger.debug(f"已更新「tpcosmo」数据库: {db}")
        r = {
            "code": 201,
            "msg": "已扫码，等待支付!",
        }

        return r

    # 付款成功
    elif r["alipay_trade_query_response"]["trade_status"] == 'TRADE_SUCCESS':
        db = r['alipay_trade_query_response']
        # 更新交易数据库
        trade_no = r["alipay_trade_query_response"]["trade_no"]
        filter = {
            'trade_no': trade_no
        }
        mongo_client['tpcosmo']['bill'].update_one(
            filter,
            {'$set': {'update_time': str(datetime.datetime.now()), **db}},
            upsert=True
        )
        logger.debug(f"已更新「bill」数据库: {db}")

        # 更新预创建付款数据库
        out_trade_no = r["alipay_trade_query_response"]["out_trade_no"]
        filter = {
            'out_trade_no': out_trade_no
        }
        db = {
            'status': '付款成功',
            'trade_no': trade_no,
            # 'is_live': 0,
        }
        mongo_client['tpcosmo']['create_bill'].update_one(
            filter,
            {'$set': {'update_time': str(datetime.datetime.now()), **db}},
            upsert=True
        )
        logger.debug(f"已更新「create_bill」数据库: {db}")
        # 查询预创建订单信息
        bill_info = mongo_client['tpcosmo']['create_bill'].find_one(
            filter,
            {'$set': {'update_time': str(datetime.datetime.now()), **db}},
            upsert=True
        )

        # 反转表
        subscribe_type_2_words = {
            "标准会员": "VIP",
            "教育优惠/标准会员": "edu_VIP",
            "高级会员": "Professional"
        }

        subscribe_type = subscribe_type_2_words.get(bill_info['type'])

        # 更新用户基础信息表
        filter = {'email': bill_info['user_id']}
        mongo_client['tpcosmo']['user'].update_one(
            filter,
            {'$set':
                 {
                     'update_time': str(datetime.datetime.now()),
                      'user_type': subscribe_type,
                 }
            }
        )
        # 更新用户金融表
        mongo_client['tpcosmo']['user_info'].update_one(
            filter,
            {
                '$set': {
                    'update_time': str(datetime.datetime.now()),
                    'total_tokens': 1,
                    'rest_token': 1,
                    'subscribe_type': subscribe_type,
                    'subscribe_start_time': str(datetime.datetime.now()),
                    'subscribe_end_timestamp': int(time.time()) + 30 * 24 * 60 * 60,
                    'subscribe_end_time': str(datetime.datetime.now() + datetime.timedelta(days=30))
                }
            }
        )
        # 更新redis

        r = {'code': 200, 'msg': 'success'}
        return r

    # 二维码已过期
    r = {
        "code": 403,
        "msg": "二维码已过期！",
    }
    return JSONResponse(content=r)


if __name__ == '__main__':
    asyncio.run(check_bill('32303233-2D30372D-30332031-303A3238-3A31322E-33333432-3733'))

