# -*- coding: utf-8 -*-
# @Time    : 2017/10/13 15:31
# @Author  : DX.Ssssssss
# @File    : sinanewssp.py
# @Software: PyCharm Community Edition

import requests
import json
import re
import pandas
import sqlite3
from bs4 import BeautifulSoup as bs

url1 = 'http://news.sina.com.cn/china/'
url2 = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20&'
url3 = 'http://news.sina.com.cn/c/nd/2017-10-13/doc-ifymvuys8881273.shtml'

# 获取文章细节
def getnewsdetail(newsurl):
    result = {}
    res = requests.get(newsurl)
    # 发送请求前打开网页源代码查看网页编码是什么
    res.encoding = 'utf-8'
    #print(res.text)
    soup = bs(res.text, 'html.parser')
    result['文章标题'] = soup.select("#artibodyTitle")[0].text
    result['时间'] = soup.select('.time-source')[0].contents[0].strip()
    result['新闻来源'] = soup.select('.time-source a')[0].text
    result['作者'] = soup.select('.article-editor')[0].text.strip("责任编辑：")
    result['文章内容'] = ' '.join([p.text.strip() for p in soup.select('#artibody p')[:-1]])
    result['评论数量'] = getCommentsCount()
    print(result)
# 获得文章ID，用于抓取评论数
def getNewsId():
    patten = re.compile('doc-i(.*).shtml',re.S)
    m = re.findall(patten, url3)[0]
    return m
# 获得评论数
def getCommentsCount():
    # newsid = re.findall(re.compile('doc-i(.*?).shtml',re.S),url3)
    #m = re.search('doc-i(.*).shtml', 'http://news.sina.com.cn/c/nd/2017-10-13/doc-ifymvuys8881273.shtml')
    #newsid = m.group(1)
    commenturl = url2.format(getNewsId())
    res = requests.get(commenturl)
    jd = json.loads(res.text.strip('var data='))
    return jd['result']['count']['total']


# def parserListLink()
if __name__ == "__main__":
    newsurl = 'http://news.sina.com.cn/c/nd/2017-10-13/doc-ifymvuys8881273.shtml'
    getCommentsCount()
    getnewsdetail(newsurl)