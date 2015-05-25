#! encoding=utf-8
import urllib2
import re
# 从http://www.xici.net.co/nn/获取最新的代理地址
def find_proxies():
    url = "http://www.xici.net.co/nn/"
    print( u"正在从%s获取代理中..." % url)
    html = urllib2.urlopen(url).read()
    boxes = re.findall('<tr class=".*?">.*?</tr>', html, re.DOTALL)
    # 存放所有的代理
    all_proxies = {}
    for box in boxes:
        exp = r'<td>(.*?)</td>'
        items = re.findall(exp, box, re.DOTALL)
        # 存放一个代理
        proxie = {}
        proxie['ip'] = items[2]
        proxie['port'] = items[3]
        proxie['position'] = items[4]
        proxie['anonymous'] = items[5]
        proxie['type'] = items[6]
        items[7] = re.search(ur'title="(.*)"',items[7]).group(1)
        proxie['speed'] = items[7]
        items[8] = re.search(ur'title="(.*)"',items[8]).group(1)
        proxie['delay'] = items[8]
        proxie['date'] = items[9]
        all_proxies[proxie['ip']] = proxie

    print (u"获取完成,获取了%d个代理" % len(all_proxies))
    return all_proxies
    # write

if __name__ == "__main__":
    find_proxies()
