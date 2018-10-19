#! /usr/bin/python
# coding='utf-8'
"""
获取京东商城商品信息爬虫
Author: zhouzying
URL: https://www.zhouzying.cn
Date: 2018-10-15
"""

from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import re


# 获取网页源代码
def main():
    product = input("请输入商品名称：")
    driver = webdriver.Chrome()

    filepath = str(product) + ".txt"
    # 商品个数计数
    i = 1
    # 页数控制
    index = 1
    # 设总页数total的初值为100
    total = 100
    while index < total:
        try:

            page = index * 2 - 1
            # 关键字中如果有中文字符，URL中需加入“&enc=utf-8”字符编码
            url = 'https://search.jd.com/Search?keyword=' + str(product) + "&enc=utf-8" + "&page=" + str(page)
            driver.get(url)
            # 执行页面向下滑至底部的动作
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            # 停顿3秒等待页面加载完毕！！！（必须留有页面加载的时间，否则获得的源代码会不完整。）
            time.sleep(3)
            html = driver.page_source

            total, i = parser(html, i, filepath)
            print("第{}页获取完成！".format(index))
            index += 1

        except RequestException:
            print(RequestException)
            
    print("关于{}的全部商品信息获取完成！".format(product))
    # 退出浏览器
    driver.quit()


# 提取商品信息
def parser(html, i, filepath):

    soup = BeautifulSoup(html, 'html5lib')

    # 总页数
    total = eval(soup.find('span', 'p-skip').em.b.text)
    # 定位到包含这些商品信息的代码
    items = soup.find_all('div', 'gl-i-wrap')

    for item in items:
        # 商品名称
        p_name = item.find('div', 'p-name').a.em.text
        # 商品价格
        p_price = item.find('div', 'p-price').strong.text

        # 店家信息
        p_shopinfo = item.find('div', re.compile('p-shop'))

        if p_shopinfo.a is None:
            p_shop = p_shopinfo.span.text
        else:
            p_shop = p_shopinfo.a.text

        # 评论数量
        p_comment = item.find('div', 'p-commit').strong.a.text
        # 写入文件

        with open(filepath, 'at', encoding="utf-8") as f:
            f.write("{}.商品名称：{}  价格：{}  店家信息：{}  评论数量：{}\n".format(i, p_name, p_price, p_shop, p_comment))

        # 可视化输出
        print("{}.商品名称：{}  价格：{}  店家信息：{}  评论数量：{}".format(i, p_name, p_price, p_shop, p_comment))
        # 统计这一页有多少商品
        i += 1
    return total, i


if __name__ == '__main__':
    main()
