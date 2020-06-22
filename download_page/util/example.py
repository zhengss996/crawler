#-*- encoding: utf-8 -*-
'''
request_test.py
Created on 2019/3/7 21:05
Copyright (c) 2019/3/7, 海牛学院版权所有.
@author: 潘牛
'''
import mx.URL, sys
from tld import get_fld
from bs4 import BeautifulSoup
from commons.util.request_util import RequestUtil
from commons.util.html_util import HtmlUtil
from commons.util.util import Util

def test_beautiful():
    r = RequestUtil()
    hu = HtmlUtil()
    u = Util()
    url = 'https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1'
    html = r.http_get_phandomjs(url)

    #html = html.decode('utf-8').encode(sys.getfilesystemencoding())
    #print html
    #可以从HTML或XML文件中提取数据的Python第三方库
    soup = BeautifulSoup(html, 'lxml')
    a_docs = soup.find_all("a")
    aset = set()
    #获取domain
    domain = get_fld(url)
    #获取host
    host = hu.get_url_host(url)
    print 'domain==>',domain
    print 'host==>',host
    for a in a_docs:
        #获取a标签的href
        a_href = get_format_url(url,a,host)
        #获取a标签的内容
        a_title = a.get_text().strip()
        if a_href == '' or a_title == '':
            continue

        if aset.__contains__(a_href):
            continue
        aset.add(a_href)
        #获取a标签的host
        a_host = hu.get_url_host(a_href)
        #获取a标签href链接url的md5
        a_md5 = u.get_md5(a_href)
        #获取a标签所对应的xpath
        a_xpath = hu.get_dom_parent_xpath_js(a)
        print ("%s\t%s\t%s\t%s\t%s") % (a_title.decode("utf-8"),a_href,a_host,a_md5,a_xpath)

def get_format_url(url,a_doc, host):
        a_href = a_doc.get('href')
        try:
            if a_href is not None and a_href.__len__() > 0:
                a_href = str(a_href).strip()
                a_href = a_href[:a_href.index('#')] if a_href.__contains__('#') else a_href
                # a_href = a_href.encode('utf8')
                # a_href = urllib.quote(a_href,safe='.:/?&=')
                if a_href.startswith('//'):
                    url = 'https:' + a_href if url.startswith('https:') else 'http:' + a_href
                    url = mx.URL.URL(str(url))
                    a_href = url.url
                elif a_href.startswith('/'):
                    url = 'https://' + host + a_href if url.startswith('https:') else 'http://' + host + a_href
                    url = mx.URL.URL(str(url))
                    a_href = url.url
                elif a_href.startswith('./') or a_href.startswith('../'):
                    url = mx.URL.URL(str(url) + '/' + a_href)
                    a_href = url.url
                elif not a_href.startswith('javascript') and not a_href.startswith('mailto') and not a_href.startswith('http') and a_href != '':
                    url = 'https://' + host + '/' + a_href if url.startswith('https:') else 'http://' + host + '/' + a_href
                    url = mx.URL.URL(str(url))
                    a_href = url.url
                a_href = a_href[:-1] if a_href.endswith('/') else a_href
                #a_href = a_href.lower()
            get_fld(a_href)
        except:
            return ''

        if not a_href.startswith('http'):
            return ''

        if a_href.__contains__('?'):
            a_params_str = a_href[a_href.index('?') + 1:]
            a_params = a_params_str.split('&')
            a_params.sort()
            a_params_str = '&'.join(a_params)
            a_href = a_href[:a_href.index('?') + 1] + a_params_str

        return a_href

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    test_beautiful()