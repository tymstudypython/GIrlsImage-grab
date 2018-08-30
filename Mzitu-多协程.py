# coding:utf-8
import random
import requests
from lxml import html  # 导入lxml库和html.fromStringh函数来解析html
import os
import time
from gevent import monkey
import gevent


# 头部伪装、未伪装前目标网站没有数据返回，所以伪装成浏览器
def header(referer):
    headers = {
        'Host': 'i.meizitu.net',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/59.0.3071.115 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }
    return headers


# 获取主页列表
def getPage(pageNum):
    baseUrl = 'http://www.mzitu.com/page/{}'.format(pageNum)  # 获取当前页的源代码
    selector = html.fromstring(requests.get(baseUrl).content)  # 得到源代码并解析html源代码
    urls = []
    for i in selector.xpath('//ul[@id="pins"]/li/a/@href'):  # 得到每一个专题的详情页
        urls.append(i)
    return urls


# 图片链接列表， 标题
# url是详情页链接
def getPiclink(url):
    sel = html.fromstring(requests.get(url).content)
    # 图片总数
    total = sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    # 标题
    title = sel.xpath('//h2[@class="main-title"]/text()')[0]
    # 接下来的链接放到这个列表
    jpgList = []
    for i in range(int(total)):
        # 每一页
        link = '{}/{}'.format(url, i+1)
        s = html.fromstring(requests.get(link).content)
        # 图片地址在src标签中
        jpg = s.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
        # 图片链接放进列表
        jpgList.append(jpg)
    return title, jpgList


# 下载图片
def downloadPic(sums, urls):
    k = 1
    # 图片数量
    count = len(urls)
    # 文件夹格式
    dirName = "【%sP】%s" % (str(count), sums)
    # 新建文件夹
    os.mkdir(dirName)
    for i in urls:
        # 文件写入的名称：当前路径／文件夹／文件名
        filename = '%s/%s/%s.jpg' % (os.path.abspath('.'), dirName, k)
        print('开始下载图片:%s 第%s张' % (dirName, k))
        with open(filename, "wb+") as jpg:
            jpg.write(requests.get(i, headers=header(i)).content)  # 调用header函数，得到伪装请求
            time.sleep(random.random())  # 随机睡眠时长,减小被发现几率,默认随机[0,1)
        k += 1

if __name__ == '__main__':
    pageNum = input('请输入页码：')
    # for link in getPage(pageNum):
    monkey.patch_all()
    listurl=[]
    for i in getPage(pageNum):
        sums, urls = getPiclink(i)
        listurl.append(gevent.spawn(downloadPic, sums, urls))
    gevent.joinall(listurl)