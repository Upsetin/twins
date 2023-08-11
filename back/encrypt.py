import base64
import hashlib
from Crypto.Cipher import AES


iv = 'Xi7ITU1AuG9r6dNj'  # 偏移量
key = 'Veys8Jgn1n7LHOe7'  # 密钥


def get_hash(key: str):
    value = hashlib.sha256(key.encode()).hexdigest().upper()
    return value


# 补足字节方法
def pad(value):
    BLOCK_SIZE = 16  # 设定字节长度
    count = len(value)
    if (count % BLOCK_SIZE != 0):
        add = BLOCK_SIZE - (count % BLOCK_SIZE)
    else:
        add = 0
    text = value + ("\0".encode() * add)  # 这里的"\0"必须编码成bytes，不然无法和text拼接
    return text


# 将明文用AES加密
def AES_en(data):
    # 将长度不足16字节的字符串补齐
    data = pad(data.encode())  # 注意在这个地方要把传过来的数据编码成bytes，不然还是会报上面说的那个错
    # 创建加密对象
    AES_obj = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    # 完成加密
    AES_en_str = AES_obj.encrypt(data)
    # 用base64编码一下
    AES_en_str = base64.b64encode(AES_en_str)
    # 最后将密文转化成字符串
    AES_en_str = AES_en_str.decode("utf-8")
    return AES_en_str


def AES_de(data):
    # 解密过程逆着加密过程写
    # 将密文字符串重新编码成二进制形式
    data = data.encode("utf-8")
    # 将base64的编码解开
    data = base64.decodebytes(data)
    # 创建解密对象
    AES_de_obj = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    # 完成解密
    AES_de_str = AES_de_obj.decrypt(data)
    # 去掉补上的空格
    AES_de_str = AES_de_str.strip()
    # 对明文解码
    AES_de_str = AES_de_str.decode("utf-8")
    return AES_de_str.strip(b'\x00'.decode())  # 去除特定的空格


if __name__ == '__main__':

    data = "{'text':'我在成都！', 'type_id': 'ca2ea52e48c39d45592bc6d9ec362389944c5b536e7b32e5eb1af1c7da512731'}"  # 测试数据
    b = AES_en(data)
    print(f"加密为：{b}")  # 此写法python3.6以上才支持
    raw_data = AES_de(b)
    print(f'解密为：{raw_data}')
    encrypt_data = 'Hhjtqr7huXnlVA/UdkQHv8gPofOSCSbpDPlJyHQsdZG6FAlnr6vpahxuaPB07mrJtNY8Uk1Xc3Y5h+HqM5bIaWBnIJl8PtDx44Cc5xz8kHyaqkIJAuzF5PfDdsZnXIgG'
    r = AES_de(encrypt_data)
    print(eval(r))

