# !/usr/bin/env python
# coding=utf-8

import asyncio
import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pyppeteer import launch

from common import *

HTML = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
</head>
<body>
    <div align="center">
        <h2>😘 Daily</h2>
        <p>傻宝宝，今天已经是我们相恋的第 {loving_days} 天了喔 💓。</p>
        <br/>
        <img style="padding: 0.60em; background: white; box-shadow: 1px 1px 10px #999;" src="cid:one" />
    </div>
</body>
</html>
"""
IMAGE_NAME = "one.png"


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
    html_content = HTML.replace("{loving_days}", str(get_loving_days()))

    msg = MIMEMultipart("alternative")
    msg["Subject"] = Header("😘 男朋友的日常问候", MAIL_ENCODING )
    msg["From"] = Header("暖宝宝", MAIL_ENCODING)
    msg["To"] = Header("小仙女")

    with open(IMAGE_NAME, "rb") as f:
        img = MIMEImage(f.read())
        img.add_header("Content-ID", "one")
        msg.attach(img)
    msg.attach(MIMEText(html_content, "html", MAIL_ENCODING))

    try:
        smtp_obj = smtplib.SMTP_SSL(MAIL_HOST)
        smtp_obj.login(MAIL_USER, MAIL_PASS)
        smtp_obj.sendmail(MAIL_SENDER, [MAIL_RECEIVER], msg.as_string())
        smtp_obj.quit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(fetch())
    except Exception:
        asyncio.get_event_loop().run_until_complete(fetch())
    send_email()
