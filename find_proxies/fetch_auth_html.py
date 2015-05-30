#! encoding=utf-8
import requests

def fetch_auth_html():
#    data = {'user':'954229335@qq.com','passwd':'xrgs!b&renren'}
    url = 'http://3g.renren.com/getfriendlist.do?'
    headers = {'User-Agent': 'alexkh'}
    he= [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
    cookie = dict(alxn = '7f7c9bb6288b4b7de042842322b7871b5d80914c017cacf',
                  cp_config = '2',
                  mt = 'uJ325Mn-Smjp716JX0S2ja')
    proxies = {
        'http' : '124.200.38.46:8118'
    }
    r = requests.get(url,headers = headers, cookies = cookie, proxies = proxies)
    print r.text.encode('gbk','ignore')

if __name__ == '__main__':
    fetch_auth_html()
