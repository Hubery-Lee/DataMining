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

# 邮件内容
CONTENT_FORMAT = (
    "胖彭😄 :\n\n\t"
    "今天是 {_date}，{_week}。\n\t"
    "首先，今天已经是我们相识的第 {_loving_days} 天了喔 💓。然后我就要来播送天气了！！\n\n\t"
    "👧 {_g_city}，今天气温{_g_weather_temperature}，{_g_weather_type}，{_g_weather_dressing_index}！！\n\t"
    "{_g_weather_dressing_advice}！！\n\n\t"
    "明天，气温{_g_weather_temperature_f},{_g_weather_type_f}\n\n\t"

    # "👦 {_b_city}明天{_g_weather_temperature}，{_g_weather_type}，{_g_weather_dressing_index}！！\n\t"
    # "{_b_weather_notice}"
)

ANGRY_MSG = "😠 傻小胖，这傻逼接口他妈的又挂了喔！"


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

    if girl :
        return CONTENT_FORMAT.format(
            _date=girl_weather_today['date_y'],
            _week=girl_weather_today['week'],
            _loving_days=get_loving_days(),
            _g_city=girl_weather_today['city'],
            _g_weather_temperature =girl_weather_today['temperature'],
            _g_weather_type=girl_weather_today["weather"],
            _g_weather_dressing_index=girl_weather_today['dressing_index'],
            _g_weather_dressing_advice=girl_weather_today['dressing_advice'],
            _g_weather_temperature_f=girl_weather_future['temperature'],
            _g_weather_type_f=girl_weather_future["weather"],
            # _b_city=BOY_CITY,
            # _b_weather_high=boy_weather["high"],
            # _b_weather_low=boy_weather["low"],
            # _b_weather_type=boy_weather["type"],
            # _b_weather_notice=boy_weather["notice"],
        )



def send_email():
    """
    发送邮件
    """
    content = get_weather_info() or ANGRY_MSG
    message = EmailMessage()
    # message["from"] = address("a handsome soul","hrbeulh","126.com")
    # message["to"] = (address("my little bird","1306504695","qq.com"),address("a handsome soul","hrbeulh","126.com"))
    message["from"] = Address("a handsome soul","913304155","qq.com")
    message["to"] = (Address("my little bird","hrbeulh","126.com"),Address("a handsome soul","hrbeulh","126.com"))
    message["Subject"] = "😘 男朋友的日常问候"
    message.set_content(content)
    try:
        smtp_obj = smtplib.SMTP_SSL(MAIL_HOST)
        smtp_obj.login(MAIL_USER, MAIL_PASS)
        smtp_obj.send_message(message)
        smtp_obj.quit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    send_email()
