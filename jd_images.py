#! /usr/bin/python
# coding='utf-8'
"""
获取京东商城商品图片的Python爬虫。输入商品的名称，便可以获取该商品的全部图片到本地。
Author: 志颖
URL：www.zhouzying.cn
Data: 2018-10-15
"""
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import re
import os


# 主函数
def main():
    # 获取商品名称
    search_p = input("请输入您要获取图片的商品名称：")

    # 设定总页数total的初值为100
    total = 100
    # 文件存储位置
    path = make_new_dir(search_p)
    # 页数控制
    index = 1
    print("......正在获取图片......")
    driver = webdriver.Firefox()
    while index <= total:

        try:
            print("正在获取第{}页》》》".format(index))
            page = index * 2 - 1
            url = "https://search.jd.com/Search?keyword=" + str(search_p) + "&enc=utf-8&page=" + str(page)
            driver.get(url)
            # 执行页面向下滑至底部的动作
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            # 停顿5秒等待页面加载完毕！！！（必须留有页面加载的时间，否则获得的源代码会不完整。）
            time.sleep(5)
            html = driver.page_source
            if index == 1:

                total = get_page_numbs(html)
            items = parse_html_page(html)

            download(items, index, path)
            print("第{}页获取成功！".format(index))
            index += 1

        except:
            print('爬取失败！')

    print("关于{}的全部商品信息获取完成！".format(search_p))
    # 退出浏览器
    driver.quit()


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

    path = path + "/第" + str(index + 1) + "页"
    i = 1
    for item in items:
        # 图片地址
        uri = "https:" + str(item)
        # 匹配图片文件的后缀名
        filepath = path + str(i) + '.' + item.split('.')[-1]
        try:
            urlretrieve(uri, filepath)
            i += 1

        except:
            print("下载发生异常！")
            break


# 定义一个函数来获取商品的页面数量
def get_page_numbs(html):

    soup = BeautifulSoup(html, 'html5lib')
    pattern = '<i>(.*?)</i>'
    ls = re.findall(pattern, str(soup.find_all('span', 'fp-text')))
    # 用eval()函数取出整数
    total = eval(ls[0])
    return total


if __name__ == '__main__':
    # 计算程序运行时间
    time.clock()
    main()
    print("获取图片成功！\n")
    print("程序运行时间为{}".format(time.clock()))
    
