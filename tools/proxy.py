#! encoding=utf-8
import urllib2
import re
import logging
logging.basicConfig(filename='proxy.log', filemode='w', level=logging.DEBUG)
"""
author: sunder
date: 2015/6/9
function: renew proxies from http://www.xici.net.co/ and write it to proxies.dat
            get proxies from proxies.dat
"""

proxies_filename = 'proxies.dat'
"""
从网站上重新获取代理
"""
def renew():
    of = open(proxies_filename, 'w')

    for position in ['nn','wn']:
        url = "http://www.xici.net.co/" + position
        logging.info(u"正在从%s获取代理" % url)
        try:
            html = urllib2.urlopen(url).read()
            boxes = re.findall('<tr class=".*?">.*?</tr>', html, re.DOTALL)
            # 存放所有的代理
            proxieslist = []
            for box in boxes:
                exp = r'<td>(.*?)</td>'
                items = re.findall(exp, box, re.DOTALL)
                # 存放一个代理
                proxy = {}
                proxy['ip'] = items[2]
                proxy['port'] = items[3]
                proxy['position'] = items[4]
                proxy['anonymous'] = items[5]
                proxy['type'] = items[6]
                items[7] = re.search(ur'title="(.*)"',items[7]).group(1)
                proxy['speed'] = items[7]
                items[8] = re.search(ur'title="(.*)"',items[8]).group(1)
                proxy['delay'] = items[8]
                proxy['date'] = items[9]
                proxieslist.append(proxy['type']+'='+proxy['ip']+':'+proxy['port'])
                of.write('%s=%s:%s\n' % (proxy['type'], proxy['ip'], proxy['port']))
        except Exception as e:
            logging.info(e)
        finally:
            logging.info(u"获取了%d个代理" % len(proxieslist))
            of.close()
            return proxieslist

"""
从proxies.dat中读入proxies，并返回
"""
def get():
    # 读入proxy
    proxieslist = []
    try:
        logging.debug('open proxies.dat')
        f = open('proxies.dat', 'r')
        for line in f:
            proxieslist.append(line.strip())
        f.close()
        logging.debug('close proxies.dat')
        return proxieslist
    except IOError as e:
        logging.debug('open proxies.dat failed')
        renew()
if __name__ == "__main__":
    get()
