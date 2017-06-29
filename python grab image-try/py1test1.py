#coding=utf-8
import urllib
import re

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getImg(html):
    reg = 'src="(.+?\.jpg)"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    imglist = f7(imglist)
    x = 1
    for imgurl in imglist:
        urllib.urlretrieve(imgurl,"%s.jpg" %x)
        x+=1
    return imglist

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]



html = getHtml("https://www.etsy.com/search?q=table")
print getImg(html)
