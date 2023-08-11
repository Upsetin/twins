'''
    聊天模块:   聊天回复、聊天log记录、聊天信息搜索、聊天缓存、额度扣减、chat-id维护
    消费模块:   成为会员、消费记录、兑换码、订单查询
    用户模块:   个人信息、会员信息、认证信息、头像、昵称
    教育认证:   邮箱认证、学生卡人工通道认证「是否加急」
    额度管理:   额度更新「体验、当日、当月」、额度token记录
    登陆模块:   注册、登陆、登陆信息
    其他模块:   反馈、商务合作
'''
import base64
import datetime
import io
import re
import xml.etree.ElementTree as ET
from urllib.parse import parse_qs, urlparse

import qrcode


# 将url参数转为dict
def parse_query_params(requests_param):
    parsed_url = urlparse(requests_param)
    print(parsed_url)
    query_params = parse_qs(parsed_url.path)
    print(query_params)
    params_dict = {key: value[0] for key, value in query_params.items()}
    return params_dict


# 生成二维码
def make_qr_img(data: str):
    # 生成二维码
    img = qrcode.make(data)

    # 将图像转换为二进制
    byte_stream = io.BytesIO()
    img.save(byte_stream)

    # 获取二进制内容
    binary_img = byte_stream.getvalue()

    # 将二进制流转换为Image对象
    # image_stream = io.BytesIO(binary_img)
    # img = Image.open(image_stream)

    # 展示图像
    # img.show()

    # 将图像转换为Base64编码
    base64_img = base64.b64encode(binary_img).decode('utf-8')

    # print("二进制数据:", binary_img[:50], "...")
    # print("Base64编码:", base64_img)

    return base64_img


# 生成id
def make_uuid():
    time_stamp = str(datetime.datetime.now())
    print(time_stamp)

    r = time_stamp.encode().hex().upper()
    print(r)

    r = '-'.join(r[i:i + 8] for i in range(0, len(r), 8))

    print(r)
    return r


# xml、json互转
def xml_to_json(xml_string):
    element = ET.fromstring(xml_string)
    dict_data = {}
    if len(element.attrib) > 0:
        dict_data["@attributes"] = element.attrib
    if element.text:
        dict_data["text"] = element.text.strip()
    for child in element:
        child_data = element_to_dict(child)
        if child.tag in dict_data:
            if type(dict_data[child.tag]) is list:
                dict_data[child.tag].append(child_data)
            else:
                dict_data[child.tag] = [dict_data[child.tag], child_data]
        else:
            dict_data[child.tag] = child_data

    for i, j in dict_data.items():
        if type(j) == dict and j.get('text'):
            dict_data[i] = j.get('text')

    return dict_data


def element_to_dict(element):
    dict_data = {}
    if len(element.attrib) > 0:
        dict_data["@attributes"] = element.attrib
    if element.text:
        dict_data["text"] = element.text.strip()
    for child in element:
        child_data = element_to_dict(child)
        if child.tag in dict_data:
            if type(dict_data[child.tag]) is list:
                dict_data[child.tag].append(child_data)
            else:
                dict_data[child.tag] = [dict_data[child.tag], child_data]
        else:
            dict_data[child.tag] = child_data
    return dict_data


# 检测是否为教育邮箱
def is_educational_email(email):
    # 定义教育邮箱的正则表达式
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(edu|edu\.[a-zA-Z]{2,})$"
    # 判断邮箱是否匹配正则表达式
    if re.match(pattern, email):
        return True
    else:
        return False


if __name__ == '__main__':
    email = '1@stu.edu.test.edusss.com'
    r = is_educational_email(email)

    print(r)

    # make_qr_img('https://qr.alipay.com/bavh4wjlxf12tper3a')
    #
    # r = make_uuid()
    #
    # print(r)
