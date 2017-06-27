# coding=utf-8
import requests
import re
from lxml import etree
import time
import sys
import urllib
reload(sys)
sys.setdefaultencoding("utf-8")
 
#定义一个爬虫
class spider(object):
    def __init__(self):
        print u'开始爬取内容。。。'
 
#getsource用来获取网页源代码
    def getsource(self,url):
        html = requests.get(url)
        return html.text
 
#changepage用来生产不同页数的链接
    def changepage(self,url,total_page):
        now_page = int(re.search('page=(\d+)',urll,re.S).group(1))   #可修改
        page_group = []
        for i in range(now_page,total_page+1):
            link = re.sub('page=\d+','page=%s'%i,urll,re.S)       #可修改
            page_group.append(link)
        return page_group
 
#getpic用来爬取一个网页图片
    '''
    def getpic(self,source):
        selector = etree.HTML(source)
        #pic_url = selector.xpath('//ul[@class="ali"]/li/div/a/img/@src')   #可修改
        pic_url = selector.xpath('//ul[@class="ali"]/li/div/a/img/@src')
        return pic_url
    '''
    def getImg(html):
        reg = 'src="(.+?\.jpg)" '
        imgre = re.compile(reg)
        imglist = re.findall(imgre,html)
        x = 100
        for imgurl in imglist:
            urllib.urlretrieve(imgurl,'%s.jpg' % x)
            x+=1
        return imglist

#savepic用来保存结果到pic文件夹中
    def savepic(self,pic_url):
        picname=re.findall('(\d+)',link,re.S)    #可修改
        picnamestr = ''.join(picname)
        i=0
        for each in pic_url:
            print 'now downloading:' + each
            pic = requests.get(each)
            fp = open('pic\\'+picnamestr +'-'+str(i)+ '.jpg', 'wb')
            fp.write(pic.content)
            fp.close()
            i += 1
 
#ppic集合类的方法
    def ppic(self, link):
        print u'正在处理页面：' + link
        html = picspider.getsource(link)
        pic_url = picspider.getImg(html)
        picspider.savepic(pic_url)
 
time1=time.time()
if __name__ == '__main__':
    url = 'https://www.etsy.com/il-en/search?q=furniture'#可修改
    urll= 'https://www.etsy.com/search?q=furniture&explicit=1&'
    picspider = spider()
    all_links = picspider.changepage(url,3)     #可修改
    for link in all_links:
        picspider.ppic(link)
time2=time.time()
print u'耗时:'+str(time2-time1)

