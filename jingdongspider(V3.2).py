# March 22,2018 Author: Zhiying Zhou
# Updated April 19,2018 Author: Zhiying Zhou
# Updated April 20,2018 added making new directory automatically according to the words that you searched.
from requests.exceptions import RequestException
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import re
import os


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
    soup = BeautifulSoup(html, 'lxml')
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


# 创建一个与商品名称对应的文件夹
def make_new_dir(name):
    file_path = "/home/zhiying/图片/" + str(name)
    os.mkdir(file_path)
    return file_path


# 以页为单位下载图片并保存到本地
def download(items, index, path):
    for i in range(len(items)):
        uri = "https:" + str(items[i])
        # 图片的存放位置
        path = path + "/" + "第" + str(index + 1) + "页" + str(i + 1) + ".jpg"
        # 异常处理
        try:
            urlretrieve(uri, filename=path)
        except:
            pass


# 定义一个函数来获取商品的页面数量
def get_page_numbs(url):
    html = get_html_page(url)
    soup = BeautifulSoup(html, 'html5lib')
    pattern = '<i>(.*?)</i>'
    ls = re.findall(pattern, str(soup.find_all('span', 'fp-text')))
    # 用eval()函数取出整数
    length = eval(ls[0])
    return length


def main():
    # 获取商品名称
    search_p = input("请输入您要获取图片的商品名称：")

    # 构造网址
    url = "https://search.jd.com/Search?keyword=" + str(search_p) + "&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=" + \
          str(search_p) + "&page=" + str(1)
    # 总的页面数量
    page_nums = get_page_numbs(url)
    print("......正在获取图片......")
    # 开始从第一页爬取图片
    for index in range(page_nums):
        url = "https://search.jd.com/Search?keyword=" + str(search_p) + "&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=" + \
         str(search_p) + "&page=" + str(index * 2 + 1)
        print("正在获取第%s页》》》" % (index + 1))
        html = get_html_page(url)
        download(parse_html_page(html), index, make_new_dir(search_p))
        print("第%s页获取成功！" % (index + 1))


if __name__ == '__main__':
    # 计算程序运行时间
    time.clock()
    main()
    print("获取图片成功！\n")
    print("程序运行时间为{}".format(time.clock()))



