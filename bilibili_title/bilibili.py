# -*- coding:utf-8 -*-

import urllib2
import urllib
import re
import socket
# 设置超时，根据需要修改，现在设置为5秒
socket.setdefaulttimeout(5)

def bilibili(start_av_number, end_av_number):
    print u'任务开始'
    url_head = r'http://www.bilibili.com/video/av'
    filename = str(start_av_number) + '_' + str(end_av_number) + '.txt'
    my_file = open(filename,'a')
    for av_number in range(start_av_number, end_av_number+1):
#        if (av_number - start_av_number + 1)%20 == 0:
#            print u'目前已完成',
#            print av_number,1.0*(av_number-start_av_number+1)/(av_number - start_av_number + 1)
        print av_number,
        title = ''
        try:
            url = url_head + str(av_number) + '/'
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            values = {'name' : 'Michael Foord',
                    'location' : 'Northampton',
                    'language' : 'Python' }
            headers = { 'User-Agent' : user_agent }

            data = urllib.urlencode(values)
            req = urllib2.Request(url, data, headers)
            response = urllib2.urlopen(req)
            the_page = response.read()

            html = the_page.decode('utf-8','ignore')
            exp = r'<h2 title="(.*)">.*</h2>'
            title = re.search(exp, html).group(1)
        except:
            title = ''
        print title.encode('gbk','ignore')
        line = str(av_number) + '\t' + title.encode('utf-8','ignore') + '\n'
        my_file.write(line)
    my_file.close()
    print u'任务完成'

if __name__ == '__main__':
    # 修改这里的参数来改变访问的网页范围
    start_av_number = 2200000
    end_av_number = 2289000
    bilibili(start_av_number,end_av_number)
