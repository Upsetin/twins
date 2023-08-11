import qrcode
from io import BytesIO

import uvicorn
from fastapi import FastAPI, Response, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import requests
import urllib.parse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

WECHAT_APPID = "wxe59bf8bfee088d72"
WECHAT_SECRET = "6a03758acc1cbb63bcad112f54261868"
REDIRECT_URI = "https://api.multicosmo.com/wchat_callback"


@app.get("/")
async def home(request: Request):
    authorize_url = f"https://open.weixin.qq.com/connect/oauth2/authorize?appid={WECHAT_APPID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
    authorize_url = f'https://open.weixin.qq.com/connect/oauth2/authorize?appid={WECHAT_APPID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect&forcePopup=true'
    print(authorize_url)
    return templates.TemplateResponse("home.html", {"request": request, "authorize_url": authorize_url})


import tempfile

@app.get("/qrcode")
async def generate_qrcode():
    authorize_url = f"https://open.weixin.qq.com/connect/oauth2/authorize?appid={WECHAT_APPID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"

    # 生成二维码
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(authorize_url)
    qr.make(fit=True)

    # 创建二维码图片
    image = qr.make_image(fill_color="black", back_color="white")

    # 创建临时文件并保存图片
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file_path = tmp_file.name
        image.save(tmp_file_path)

    # 返回二维码图片
    return FileResponse(tmp_file_path, media_type="image/png")



@app.get("/wchat_callback")
async def callback(request: Request, response: Response, code: str):
    # 通过授权码获取访问令牌和openid
    token_url = f"https://api.weixin.qq.com/sns/oauth2/access_token?appid={WECHAT_APPID}&secret={WECHAT_SECRET}&code={code}&grant_type=authorization_code"
    token_response = requests.get(token_url)
    token_data = token_response.json()
    print('token_data:', token_data)
    access_token = token_data["access_token"]
    openid = token_data["openid"]

    # 使用访问令牌和openid获取用户信息
    user_info_url = f"https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN"
    user_info_response = requests.get(user_info_url)
    user_info_data = user_info_response.json()

    print('user_info_data:', user_info_data)
    print('headimgurl:', user_info_data['headimgurl'])
    print('nickname:', user_info_data['nickname'])
    print('openid:', user_info_data['openid'])


    # 在这里编写注册逻辑，将用户信息保存到数据库或进行其他操作

    # 用户关注公众号
    subscribe_url = f"https://api.weixin.qq.com/cgi-bin/user/info/updateremark?access_token={get_mp_access_token()}&openid={openid}&remark=registered"
    r = requests.post(subscribe_url)
    print('r:', r.text)


    # 返回用户信息
    return templates.TemplateResponse("user_info.html", {"request": request, "user_info": user_info_data})


def get_mp_access_token():
    # 获取公众号访问令牌
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APPID}&secret={WECHAT_SECRET}"
    token_response = requests.get(token_url)
    token_data = token_response.json()
    access_token = token_data["access_token"]
    return access_token


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8008)
