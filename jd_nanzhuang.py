#! /usr/bin/python
# coding="utf-8"
# March 22,2018 Author: zhouzying
# Updated Oct 15,2018 Author
# 获取京东商城男装商品全部图片
from requests.exceptions import RequestException
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from multiprocessing import Pool
import time
from selenium import webdriver


# 获取网页源代码
def get_html_page(url):
    try:
        driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(5)
        # 执行页面向下滑至底部的动作
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        # 停顿5秒等待页面加载完毕！！！（必须留有页面加载的时间，否则获得的源代码会不完整。）
        time.sleep(5)
        html_sourcode = driver.page_source
        driver.close()
        return html_sourcode
    except RequestException:
        print(RequestException)


# 提取网页的图片的网址
def parse_html_page(html):

    # 对有效图片网址进行提取
    soup = BeautifulSoup(html, 'html5lib')
    # 定义一个列表来获取分析得到的图片的网址

    url_items = []
    li_tags = soup.find_all('li', 'gl-item')
    for li_tag in li_tags:
        try:
            if len(li_tag.img["src"]) >= 10:
                url_items.append(li_tag.img['src'])
            else:
                pass
        except:
            if len(li_tag.img["data-lazy-img"]) >= 10:
                url_items.append(li_tag.img['data-lazy-img'])
            else:
                url_items.append(li_tag.img["src"])

    return url_items


# 以页为单位下载图片并保存到本地
def download(items, index):
    for i in range(len(items)):
        uri = "https:" + str(items[i])
        path = "/home/zhiying/图片/jd/" + "第" + str(index + 1) + "页" + str(i + 1) + ".jpg"
        # 异常处理
        try:
            urlretrieve(uri, filename=path)
        except:
            pass


def main(index):
    # 构造网址

    url = "https://search.jd.com/Search?keyword=男装&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=男装&cid2=1342&page=" + \
           str(index * 2 + 1)
    print("正在获取第%s页》》》" % (index + 1))
    html = get_html_page(url)
    download(parse_html_page(html), index)
    print("第%s页获取成功！" % (index + 1))


if __name__ == '__main__':
    # 计算程序运行时间
    time.clock()
    pool = Pool()
    pool.map(main, (index for index in range(100)))
    print("获取图片成功！\n")
    print("程序运行时间为{}".format(time.clock()))
