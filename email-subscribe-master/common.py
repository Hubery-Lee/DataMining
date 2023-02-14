# !/usr/bin/env python
# coding=utf-8

import os
import datetime

FALL_IN_LOVE = (2019, 8, 20)
MAIL_HOST = "smtp.126.com"
MAIL_USER = "hrbeulh@126.com"
MAIL_PASS = "lihui123"
MAIL_SENDER = "hrbeulh@126.com"
MAIL_RECEIVER = "913304155@qq.com"
#MAIL_RECEIVER = "1306504695@qq.com"

MAIL_ENCODING = "utf8"


def get_loving_days():
    """
    获取恋爱天数
    """
    today = datetime.datetime.today()
    anniversary = datetime.datetime(*FALL_IN_LOVE)
    return (today - anniversary).days
