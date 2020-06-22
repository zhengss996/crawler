#-*- encoding: utf-8 -*-
'''
xpath_test.py
Created on 2019/3/16 20:23
Copyright (c) 2019/3/16, 海牛学院版权所有.
@author: 潘牛
'''

import mx.URL,sys
from tld import get_tld
from bs4 import BeautifulSoup
from lxml import etree
from commons.util.request_util import RequestUtil
from commons.util.html_util import HtmlUtil
from commons.util.util import Util



if __name__ == '__main__':
    r = RequestUtil()
    hu = HtmlUtil()
    u = Util()
    url = 'https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1'
    html = r.http_get_phandomjs(url)


    dom_tree = etree.HTML(html)


    ###XPath匹配
    a_text = dom_tree.xpath("//div[@id='d_list']/ul[5]/li[2]/span[contains(@class,'c_tit')]/a[1]/text()")
    a_href = dom_tree.xpath("//div[@id='d_list']/ul[8]/li[3]/span[2]/a/@href")
    print a_text[0]
    print a_href[0]

    #--------本地测试-----------------------
    # myPage = '''<html>
    #     <title>TITLE</title>
    #     <body>
    #     <h1>我的博客</h1>
    #     <div>我的文章</div>
    #     <div id="photos">
    #      <img src="pic1.jpeg"/>
    #      <span id="pic1">PIC1 is beautiful!</span>
    #      <img src="pic2.jpeg"/>
    #      <span id="pic2">PIC2 is beautiful!</span>
    #      <p><a href="http://www.example.com/more_pic.html">更多美图</a></p>
    #      <a href="http://www.baidu.com">去往百度</a>
    #      <a href="http://www.163.com">去往网易</a>
    #      <a href="http://www.sohu.com">去往搜狐</a>
    #     </div>
    #     <p class="myclassname">Hello,\nworld!<br/>-- by Adam</p>
    #     <div class="foot">放在尾部的其他一些说明</div>
    #     </body>
    #     </html>'''
    #
    # html = etree.fromstring(myPage)
    # a_text = html.xpath("//div[@id='photos']/img[2]/@src")
    # span_text = html.xpath("//div[@id='photos']/span[1]/text()")
    #
    # print a_text[0]
    # print span_text[0]