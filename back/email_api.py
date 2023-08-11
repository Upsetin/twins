import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from loguru import logger


def send_eamil(RECIPIENT = 'kuicily@icloud.com', message: str = '您正在进行TwinParticle教育认证\n\n验证码是6923,5分钟内有效'):

    # 邮件配置
    SMTP_SERVER = 'smtp.exmail.qq.com'  # 腾讯企业邮箱SMTP服务器地址
    SMTP_PORT = 465  # 腾讯企业邮箱SMTP服务器端口号
    SMTP_USERNAME = 'auth@multicosmo.com'  # 发件人邮箱
    SMTP_PASSWORD = 'pkZXjYdBsEXSaD9z'  # 发件人邮箱密码
    # RECIPIENT = 'kuicily@icloud.com'  # 收件人邮箱
    # RECIPIENT = 'admin@multicosmo.com'

    # 构造邮件内容
    subject = '「TwinParticle」教育认证'  # 邮件主题
    # message = '您正在进行TwinParticle教育认证\n验证码是6923,5分钟内有效'  # 邮件正文

    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = RECIPIENT
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    logger.info('正在尝试发送邮件...')
    # 发送邮件
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        logger.success(f'邮件发送成功 -> {RECIPIENT}')
        return True
    except Exception as e:
        logger.erro(f"邮件发送失败 -> {RECIPIENT}| {e}")
        return False


if __name__ == '__main__':
    send_eamil('monsieur.kong@icloud.com')
