# !/usr/bin/env python
# coding=utf-8
import os
import datetime
import smtplib
import time
from email.message import EmailMessage
from email.headerregistry import Address

import requests
from urllib.parse import unquote,quote
from tenacity import retry, stop_after_attempt, wait_random
from email.utils import make_msgid

import asyncio
from pyppeteer import launch

#from common import *

FALL_IN_LOVE = (2019, 10, 5)
MAIL_HOST = "smtp.qq.com"
MAIL_USER = "913304155@qq.com"
MAIL_PASS = "qunhohukcweibfee"

MAIL_ENCODING = "utf8"


def get_loving_days():
    """
    获取恋爱天数
    """
    today = datetime.datetime.today()
    anniversary = datetime.datetime(*FALL_IN_LOVE)
    return (today - anniversary).days


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}

GIRL_CITY,  BOY_CITY = "南京","太原"
#print(quote(GIRL_CITY))

# 聚合数据天气预报 api
key ='&key=3cbeb2cd7d35fe072df5a931d4ee68c3'
WEATHER_API = 'http://v.juhe.cn/weather/index?format=2&cityname={city}&key={key}'

HTML_FORMAT = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
</head>
<body>
    <div align="center">
        <h2>😘 蓝朋友的日常问候</h2>
        <p>胖彭，今天已经是我们相识的第 {_loving_days} 天了喔 💓。然后我就要来播送天气了！！</p>
        <p>👧 {_g_city}，今天气温{_g_weather_temperature}，{_g_weather_type}，{_g_weather_dressing_index}</p>
        <p>{_g_weather_dressing_advice}</p>
        <br/>
        <img style="padding: 0.60em; background: white; box-shadow: 1px 1px 10px #999;" src="cid:{asparagus_cid}" />
    </div>
</body>
</html>
"""
IMAGE_NAME = "one.png"
ANGRY_MSG = "😠 傻小胖，这API接口又挂了喔！"

@retry(
    stop=stop_after_attempt(5),
    retry_error_callback=lambda _: None,
    wait=wait_random(min=5, max=10),
)
def get_weather_info():
    """
    获取天气信息
    """
    girl = requests.get(WEATHER_API.format(city=quote(GIRL_CITY), key=key)).json()
    time.sleep(8)  # 延迟，避免调用频率过高
    girl_weather_today = girl['result']['today']
    girl_weather_future = girl['result']['future'][1]

    _date=girl_weather_today['date_y']
    _week=girl_weather_today['week']
    _loving_days=get_loving_days()
    _g_city=girl_weather_today['city']
    _g_weather_temperature =girl_weather_today['temperature']
    _g_weather_type=girl_weather_today["weather"]
    _g_weather_dressing_index=girl_weather_today['dressing_index']
    _g_weather_dressing_advice=girl_weather_today['dressing_advice']
    _g_weather_temperature_f=girl_weather_future['temperature']
    _g_weather_type_f=girl_weather_future["weather"]

    data =[]
    data.append(_date)
    data.append(_week)
    data.append(_loving_days)
    data.append(_g_city)
    data.append(_g_weather_temperature)
    data.append(_g_weather_type)
    data.append(_g_weather_dressing_index)
    data.append(_g_weather_dressing_advice)
    data.append(_g_weather_temperature_f)
    data.append(_g_weather_type_f)

    if girl :
        return data

#open website and screenshot

async def fetch():
    browser = await launch(
        {"args": ["--no-sandbox", "--disable-setuid-sandbox"]}
    )
    page = await browser.newPage()
    await page.goto("http://wufazhuce.com/")
    await page.screenshot(
        {
            "path": IMAGE_NAME,
            "clip": {"x": 60, "y": 120, "height": 570, "width": 700},
        }
    )
    await browser.close()

def send_email():
    """
    发送邮件
    """
    #content = get_weather_info() or ANGRY_MSG
    content = ANGRY_MSG
    data = get_weather_info()
    message = EmailMessage()
    # message["to"] = Address("a handsome soul","hrbeulh","126.com")
    message["from"] = Address("a handsome soul","913304155","qq.com")
    message["to"] = (Address("my little bird","973548890","qq.com"),Address("a handsome soul","913304155","qq.com"))
    message["Subject"] = "男朋友的日常问候"
    message.set_content(content)
    # Add the html version.  This converts the message into a multipart/alternative
    # container, with the original text message as the first part and the new html
    # message as the second part.
    asparagus_cid = make_msgid()
    message.add_alternative(HTML_FORMAT.format(
            _date=data[0],
            _week=data[1],
            _loving_days=data[2],
            _g_city=data[3],
            _g_weather_temperature =data[4],
            _g_weather_type=data[5],
            _g_weather_dressing_index=data[6],
            _g_weather_dressing_advice=data[7],
            _g_weather_temperature_f=data[8],
            _g_weather_type_f=data[9],
            asparagus_cid=asparagus_cid[1:-1]), subtype='html')
    # note that we needed to peel the <> off the msgid for use in the html.
    # Now add the related image to the html part.
    with open("one.png", 'rb') as img:
        message.get_payload()[1].add_related(img.read(), 'image', 'png',
                                         cid=asparagus_cid)
    try:
        smtp_obj = smtplib.SMTP_SSL(MAIL_HOST)
        smtp_obj.login(MAIL_USER, MAIL_PASS)
        smtp_obj.send_message(message)
        smtp_obj.quit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(fetch())
    except Exception:
        asyncio.get_event_loop().run_until_complete(fetch())
    send_email()
