#!/usr/bin/env python
#encoding=utf-8

#
# 核心思想：整个过程就是模拟人的登录和访问过程
#
import urllib, urllib2, cookielib, re, sys

class  Renren(object):
    def __init__(self,email,password):
        self.email=email
        self.password=password
        self.ENCODING = 'utf-8'
# 获取所有的好友列表的页面
    def get_friendlist_pages(self,origin_url):
        try:
            self.cookie = cookielib.CookieJar() #设置登陆cookie
            self.cookieProc = urllib2.HTTPCookieProcessor(self.cookie)
        except:
            raise
        else:
            opener = urllib2.build_opener(self.cookieProc)
            opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
            #浏览器伪装
        urllib2.install_opener(opener)
        url= origin_url #登陆人人网3g网页好友列表首页
        postdata = {
            'email':self.email,
            'password':self.password,
            }
        req = urllib2.Request(url,urllib.urlencode(postdata))
        # 存储所有的好友列表所在的页面
        friendlist_pages = []
        friendlist_frist_page = urllib2.urlopen(req).read().decode(self.ENCODING,'ignore')
        f = open('renren.html','w')
        f.write(friendlist_frist_page.encode(self.ENCODING, 'ignore'))
        f.close()
        # 获取好友列表的总页数
        total_number = 0
#        try:
        total_number = re.search(ur'第\d+/(\d+)页', friendlist_frist_page, re.DOTALL).group(1)
        total_number = int(total_number)
        print ur'共有 %d 页好友' % total_number
        # 保存第一页好友列表
        friendlist_pages.append(friendlist_frist_page)
        # 逐页获取好友列表
        for num in range(1, total_number):
            url=origin_url + '&curpage=' + str(num)
#            print url
            postdata = {
                'email':self.email,
                'password':self.password,
                }
            req = urllib2.Request(url,urllib.urlencode(postdata))
            friendlist_page = urllib2.urlopen(req).read().decode(self.ENCODING,'ignore')
            friendlist_pages.append(friendlist_page)
#        print len(friendlist_pages)
#        except:
#            print ur'好友设的隐私权限，无法访问其好友'
        return friendlist_pages

# 从好友列表中提取出好友信息
    def get_friendlist(self,friendlist_pages):
        page_number = 0
        # 保存所有好友的信息
        friends = []
        for page in friendlist_pages:
            # 每一页中的好友列表中的几位好友
            tables = re.findall(r'<table><tr valign="top">(.*?)</table>',page, re.DOTALL)
            # 每位好友的信息
            table_number = 0
            for table in tables:
                # 保存一位好友的信息
                friend = {}
                info = re.search(r'<a href=".*?id=(\d+)&amp.*?">([^<].*?)</a>', table, re.DOTALL)
                friend_id = info.group(1)
                friend_name = info.group(2)
                friend_class = ''
                try:
                    friend_class = re.search(r'<span class="gray">(.*?)</span>', table, re.DOTALL).group(1)
                except:
                    friend_class = u'未分类'
                friend['uid'] = friend_id
                friend['uname'] = friend_name
                friend['uclass'] = friend_class
                friends.append(friend)
#                print u'第 %d 页的第 %d 个好友' % (page_number,table_number)
#                print u'\tid:',friend_id.encode('gbk','ignore')
                print friend_name.encode('gbk','ignore'),
#                print u'\tclass:',friend_class.encode('gbk','ignore')
                table_number += 1
            page_number += 1
        return friends





if __name__ == "__main__":
#    print "%s %s" % (sys.argv[1], sys.argv[2])
    a=Renren('954229335@qq.com','zxrgs!b&renren')
    # 获取自己额好友列表
    origin_url = 'http://3g.renren.com/friendlist.do?'
    my_friendlist_pages = a.get_friendlist_pages(origin_url)
    my_friendlist = a.get_friendlist(my_friendlist_pages)
    # 获取好友的好友列表
    for my_friend in my_friendlist:
        url = 'http://3g.renren.com/getfriendlist.do?f=all&id=' + my_friend['uid']
        print url
        friend_friendlist_pages = a.get_friendlist_pages(url)
        friend_friendlist = a.get_friendlist(friend_friendlist_pages)



#    a.login()
#    a.friends()
