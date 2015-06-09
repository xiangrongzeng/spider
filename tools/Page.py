#!/usr/bin/env
#!encoding=utf-8

import urllib2
import urllib
import cookielib
import requests
from requests.auth import HTTPBasicAuth
import logging
logging.basicConfig(filename ='page.log', filemode='w', level=logging.DEBUG)
import random
import proxy

"""
author: sunder
date: 2015/6/9
function: 获取网页，
            普通（匿名无代理）获取网页 fetch()
            需登录信息获取网页 auth_fetch()
            匿名使用代理获取 proxy_fetch()

"""
class Page():

    def __init__(self, url):
        self.url = url

    """
        获取需要登录的网页
    """
    def auth_fetch(self, uname, passwd, domain):
        cj = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        params = {'email': uname, 'password': passwd, 'origURL': self.url, 'domain': domain}
        req = urllib2.Request(self.url, urllib.urlencode(params))
        r = opener.open(req)
        html = r.read()
        return html.decode('utf-8', 'ignore')

    """
        获取不需要登录的网页
    """
    def fetch(self):
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Host': 'www.renren.com',
                    'Origin': 'http://zhichang.renren.com',
                    'Referer': 'http://zhichang.renren.com',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'}
        r = requests.get(self.url, headers=headers)
        return r.text

    """
        用代理获取不需要登录的网页,一个代理失效时，自动切换另一个代理
    """
    def proxy_fetch(self):
        # 获取代理
        proxieslist = proxy.get()
        # 用proxy获取网页
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'}
        looptimes = 0
        while looptimes < 3 or looptimes < len(proxieslist):
            try:
                randnum = random.randint(0, len(proxieslist))
                proxyinfo = proxieslist[randnum].split('=')
                proxy = {proxyinfo[0]: proxyinfo[1]}
                logging.debug('\t%d-loops, proxy is: %s=%s ' % (looptimes+1, proxyinfo[0], proxyinfo[1]))
                r = requests.get(self.url, headers=headers, proxies=proxy, timeout=3)
                print r.status_code
                logging.debug('\tget page succeed')
                encode = r.encoding
                return r.text.encode(encode, 'ignore')
            except Exception as e:
                looptimes += 1
                logging.debug(looptimes)
                logging.debug(e)
        print u'无法获取%s' % self.url
        return False




def test_auth_fetch():
    f = open('identity.dat', 'r')
    uname = f.readline().strip()
    passwd = f.readline().strip()
    url = 'http://3g.renren.com/friendlist.do'
    domain = 'renren.com'
    page = Page(url)

def test_fetch():
    url = 'http://requests-docs-cn.readthedocs.org/zh_CN/latest/'
#    url = 'http://baike.baidu.com/view/22064.htm'
    page = Page(url)
    logging.debug(u'获取网页中')
    logging.debug(page.fetch().encode('gbk', 'ignore'))
    logging.debug(u'获取结束')

def test_proxy_fetch():
    looptimes = 100
    while looptimes > 0:
        id = looptimes + 22000
        id = str(id)
        url = 'http://baike.baidu.com/view/' + id + '.htm'
        page = Page(url)
        logging.debug(u'获取网页中')
        html = page.proxy_fetch()
        if html:
            outfile = 'g:/test_ground/tmp/' + id + '.html'
            f = open(outfile,'w')
            f.write(html)
            f.close()
        else:
            print 'need new proxies'
            looptimes = 0
        logging.debug(u'获取结束')
        looptimes -= 1

if __name__ == '__main__':
#    test_auth_fetch()
#    test_fetch()
    test_proxy_fetch()
