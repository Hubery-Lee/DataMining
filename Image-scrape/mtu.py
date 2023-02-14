import requests
import os
from hashlib import md5
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

headers = {'If-None-Match': 'W/"5cc2cd8f-2c58"',
           "Referer": "http://www.mzitu.com/all/",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 SafarMozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
#请求头的这个Referer一定要加，妹子网有反爬，反正粘贴复制就行，多加几个信息无所谓

DIR_PATH = r"F:\mzitu"

def get_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            #print(response.text)
            return response.text
        return None
    except RequestException:
        print('获取索引页失败')
        return None

def parse_page(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('#pins li')
    for link in items:
        href = link.a['href']
        alt = link.img['alt']
        make_dir(alt)
        get_detail_page(href)
    # print(items)

def get_detail_page(href):
    for i in range(1,100):
        detail_url = href + '/' + str(i)
        if requests.get(detail_url, headers=headers).status_code == 200:
            #print(detail_url)
            parse_detail_page(detail_url)
        else:
            print('已至末尾页')
            return None
 

def parse_detail_page(detail_url):
    try:
        response = requests.get(detail_url, headers=headers)
        if response.status_code == 200:
            print('获取详情页成功')
            detail_html = response.text
            # print(detail_html)
            get_image(detail_html)
        return None
    except RequestException:
        print('获取详情页失败')
        return None

def get_image(detail_html):
    soup = BeautifulSoup(detail_html, 'lxml')
    items= soup.select('.main-image')
    # print(items)
    for item in items:
        #return item.img['src']
        image = item.img['src']
        save_image(image)

def save_image(image):
   response = requests.get(image,headers=headers)
   if response.status_code == 200:
       data = response.content
       file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(data).hexdigest(), 'jpg')
       print(file_path)
       if not os.path.exists(file_path):
           with open(file_path, 'wb') as f:
               f.write(data)
               f.close()
               print('保存成功')
   else:
       print('保存失败')

def make_dir(folder_name):
    """
    新建文件夹并切换到该目录下
    """
    path = os.path.join(DIR_PATH, folder_name)
    # 如果目录已经存在就不用再次爬取了，去重，提高效率。存在返回 False，否则反之
    if not os.path.exists(path):
        os.makedirs(path)
        print(path)
        os.chdir(path)
        return True
    print("Folder has existed!")
    return False

def main():
    url = 'https://www.mzitu.com/tag/youhuo/'
    html = get_page(url)
    parse_page(html)


if __name__ == '__main__':
    main()