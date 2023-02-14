# !/usr/bin/env python
# coding=utf-8

import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText

import requests
from tenacity import retry, stop_after_attempt, wait_random

from common import *

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}

GIRL_CITY, BOY_CITY = "广州", "肇庆"

# 聚合数据天气预报 api
WEATHER_API = "https://www.sojson.com/open/api/weathera/json.shtml?city={}"

# 邮件内容
CONTENT_FORMAT = (
    "你好，傻宝宝 😄 :\n\n\t"
    "今天是 {_date}，{_week}。\n\t"
    "首先，今天已经是我们相恋的第 {_loving_days} 天了喔 💓。然后我就要来播送天气预报了！！\n\n\t"
    "👧 {_g_city}明天{_g_weather_high}，{_g_weather_low}，天气 {_g_weather_type}，"
    "{_g_weather_notice}\n\n\t"
    "👦 {_b_city}明天{_b_weather_high}，{_b_weather_low}，天气 {_b_weather_type}，"
    "{_b_weather_notice}"
)

ANGRY_MSG = "😠 傻宝宝，这傻逼接口他妈的又挂了喔！"


@retry(
    stop=stop_after_attempt(5),
    retry_error_callback=lambda _: None,
    wait=wait_random(min=5, max=10),
)
def get_weather_info():
    """
    获取天气信息
    """
    girl = requests.get(WEATHER_API.format(GIRL_CITY, headers=HEADERS)).json()
    time.sleep(8)  # 延迟，避免调用频率过高
    boy = requests.get(WEATHER_API.format(BOY_CITY, headers=HEADERS)).json()
    girl_weather = girl["data"]["forecast"][1]
    boy_weather = boy["data"]["forecast"][1]

    _date, _week = get_today(girl)

    if girl and boy:
        return CONTENT_FORMAT.format(
            _week=_week,
            _date=_date,
            _loving_days=get_loving_days(),
            _g_city=GIRL_CITY,
            _g_weather_high=girl_weather["high"],
            _g_weather_low=girl_weather["low"],
            _g_weather_type=girl_weather["type"],
            _g_weather_notice=girl_weather["notice"],
            _b_city=BOY_CITY,
            _b_weather_high=boy_weather["high"],
            _b_weather_low=boy_weather["low"],
            _b_weather_type=boy_weather["type"],
            _b_weather_notice=boy_weather["notice"],
        )


def get_today(today):
    """
    日期格式化
    """
    date = today["date"]
    week = today["data"]["forecast"][0]["date"][-3:]
    return "{}-{}-{}".format(date[:4], date[4:6], date[6:]), week


def send_email():
    """
    发送邮件
    """
    content = get_weather_info() or ANGRY_MSG
    message = MIMEText(content, "plain", MAIL_ENCODING)
    message["From"] = Header("暖宝宝", MAIL_ENCODING)
    message["To"] = Header("A handsome soul")
    message["Subject"] = Header("😘 男朋友的日常问候", MAIL_ENCODING)
    try:
        smtp_obj = smtplib.SMTP_SSL(MAIL_HOST)
        smtp_obj.login(MAIL_USER, MAIL_PASS)
        smtp_obj.sendmail(MAIL_SENDER, [MAIL_RECEIVER], message.as_string())
        smtp_obj.quit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    send_email()
