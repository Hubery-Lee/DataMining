import os
import datetime
import asyncio
import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pyppeteer import launch

FALL_IN_LOVE = (2019, 10, 5)

MAIL_HOST = "smtp.qq.com"
MAIL_USER = "913304155@qq.com"
MAIL_PASS = "o"
MAIL_SENDER = "913304155@qq.com"
MAIL_RECEIVER = "hrbeulh@126.com"
#MAIL_RECEIVER = ["973548890@qq.com","hrbeulh@126.com"]

MAIL_ENCODING = "utf8"


def get_loving_days():
    """
    获取恋爱天数
    """
    today = datetime.datetime.today()
    anniversary = datetime.datetime(*FALL_IN_LOVE)
    return (today - anniversary).days

HTML = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
</head>
<body>
    <div align="center">
        <h2>😘 nan朋友的日常问候</h2>
        <p>傻胖彭，今天已经是我们相识的第 {loving_days} 天了喔 💓。</p>
        <br/>
        <img style="padding: 0.60em; background: white; box-shadow: 1px 1px 10px #999;" src="cid:one" />
    </div>
</body>
</html>
"""
IMAGE_NAME = "one.png"


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
    html_content = HTML.replace("{loving_days}", str(get_loving_days()))

    msg = MIMEMultipart("alternative")
    msg["Subject"] = Header("😘 nan朋友的日常问候", MAIL_ENCODING )
    msg["From"] = Header("傻哥哥", MAIL_ENCODING)
    msg["To"] = Header("小仙女")

    with open(IMAGE_NAME, "rb") as f:
        img = MIMEImage(f.read())
        img.add_header("Content-ID", "one")
        msg.attach(img)
    msg.attach(MIMEText(html_content, "html", MAIL_ENCODING))

    try:
        smtp_obj = smtplib.SMTP_SSL(MAIL_HOST)
        smtp_obj.login(MAIL_USER, MAIL_PASS)
        smtp_obj.sendmail(MAIL_SENDER, MAIL_RECEIVER, msg.as_string())
        smtp_obj.quit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(fetch())
    except Exception:
        asyncio.get_event_loop().run_until_complete(fetch())
    send_email()