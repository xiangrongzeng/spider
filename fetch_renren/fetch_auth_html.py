#! encoding=utf-8
import requests

def fetch_auth_html(url, cookie, proxy):
#    data = {'user':'954229335@qq.com','passwd':'xrgs!b&renren'}
    headers = {'User-Agent': 'alexkh'}
    r = requests.get(url,headers = headers, cookies = cookie, proxies = proxy)
#    print r.text.encode('gbk','ignore')
    return r.text

if __name__ == '__main__':
    url = 'http://3g.renren.com/getfriendlist.do?'
    cookie = dict(alxn = '7f7c9bb6288b4b7de042842322b7871b5d80914c017cacf',
                  cp_config = '2',
                  mt = 'uJ325Mn-Smjp716JX0S2ja')
    proxy = {
        'http' : '124.200.38.46:8118'
    }
    fetch_auth_html(url, cookie, proxy)
