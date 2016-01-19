import http.cookiejar
import re
import urllib.request

def getOpener(head):
    # deal with the Cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

class USTB:
    def __init__(self,id,pswd):
        self.loginurl = 'http://elearning.ustb.edu.cn/choose_courses/j_spring_security_check'
        self.gradeurl = 'http://elearning.ustb.edu.cn/choose_courses/information/singleStuInfo_singleStuInfo_loadSingleStuScorePage.action'
        self.head = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64;         Trident/7.0; rv:11.0) like Gecko'
        }
        self.postdata1 = urllib.parse.urlencode({
            'j_username':str(id) + ',undergraduate',
            'j_password':pswd
        })
        self.postdata2 = urllib.parse.urlencode({
            'uid': id
        })

    def login(self):#负责登录
        opener = getOpener(self.head)
        req  = opener.open(self.loginurl, self.postdata1.encode())
        rep = req.read()
        res = re.findall('true', rep.decode('utf-8')) #确认是否登录成功,成功则返回['true'],失败为[]
        if res != []:
            return opener #成功则将opener交给getgrade方法
        else:
            return False

    def getgrade(self,opener):#负责爬取成绩
        req = opener.open(self.gradeurl, self.postdata2.encode())
        page = req.read()
        grade = re.findall('<tr.*>\s*<td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td>\s*</tr>',page.decode())
        return grade