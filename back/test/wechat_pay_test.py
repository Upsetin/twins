import uvicorn
import xmltodict
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/wechat/payment")
async def process_payment(request: Request):
    # 解析请求的XML数据
    request_data = await request.body()
    xml_data = xmltodict.parse(request_data)

    # 提取微信支付结果
    result_code = xml_data['xml']['result_code']
    return_code = xml_data['xml']['return_code']

    if result_code == 'SUCCESS' and return_code == 'SUCCESS':
        # 支付成功的处理逻辑
        # 获取订单号等相关信息
        out_trade_no = xml_data['xml']['out_trade_no']
        total_fee = xml_data['xml']['total_fee']

        # 进行支付成功后的处理操作，比如更新订单状态等

        # 返回处理结果给微信服务器
        response_data = {
            'return_code': 'SUCCESS',
            'return_msg': 'OK'
        }
    else:
        # 支付失败的处理逻辑
        # 返回处理结果给微信服务器
        response_data = {
            'return_code': 'FAIL',
            'return_msg': 'Payment failed'
        }

    # 将处理结果转换为XML格式
    response_xml = xmltodict.unparse({'xml': response_data})
    return response_xml

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
