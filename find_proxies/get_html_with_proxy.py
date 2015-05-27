#! encoding=utf-8

import urllib2

def get_html_with_proxy(ip, port, url):
    proxy_handler = urllib2.ProxyHandler({"http" : r'http://%s:%s' %(ip, port)})
    opener = urllib2.build_opener(proxy_handler)
    html = ''
    try:
        response = opener.open(url)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
    else:
        html = response.read()
#        print html.decode('utf-8')
    return html

def get_authentication_html_with_proxy(ip,port,url,user_name, password):
    proxy_handler = urllib2.ProxyHandler({"http" : r'http://%s:%s' %(ip, port)})
    auth_handler = urllib2.HTTPBasicAuthHandler()
    auth_handler.add_password(realm='PDQ Application',
                            uri=url,
                            user=user_name,
                            passwd=password)
    opener = urllib2.build_opener(auth_handler,proxy_handler)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    # ...and install it globally so it can be used with urlopen.
    urllib2.install_opener(opener)
    response = urllib2.urlopen(url)
    html = ''
    try:
        response = opener.open(url)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
    else:
        html = response.read()
#        print html.decode('utf-8')
    return html


if __name__ == '__main__':
    ip = '1.207.245.184'
    port = '80'
    url = 'http://www.guokr.com/i/0764161217/'
    user_name = 'rxiangz@gmail.com'
    password = 'zxrgs1b&guokr'
    html = get_authentication_html_with_proxy(ip,port,url,user_name,password)
    f = open('html.html','w');
    f.writelines(html)


