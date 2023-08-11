import asyncio
import datetime

import pymongo

from order import check_bill

mongo_client = pymongo.MongoClient("mongodb://White:klx5596688@8.222.210.54:27017/admin")


# 获取时间差
def get_diff_seconds(time_string: str='2023-06-13 09:46:21.533931'):
    # 获取当前时间
    current_time = datetime.datetime.now()

    # 将时间字符串中的毫秒部分去除
    time_string = time_string.split(".")[0]

    # 解析时间字符串为datetime对象
    time_object = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")

    # 计算时间差
    time_difference = current_time - time_object


    # 获取分钟差值
    seconds_difference = time_difference.total_seconds()

    # print("时间差（s）：", seconds_difference)
    if seconds_difference >= 6*60:
        return False
    return True


async def check_and_update_bill():
    # 查询数据库非支付完成账单
    db = mongo_client['tpcosmo']['create_bill'].find(
        {'status': {'$in': ['等待扫码', '等待付款']}}
    )
    for i in db:
        # print(i)
        # 过滤时间
        if get_diff_seconds(i['create_time']):
            out_trade_no = i['out_trade_no']
            await check_bill(out_trade_no=out_trade_no)

    # print(db)
    # for i in db:
    #     print(i)
    # 调用查询接口,实现账单更新
    pass


asyncio.run(check_and_update_bill())

