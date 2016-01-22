import time
import xml.etree.ElementTree as ET
import sys
import hashlib
from flask import session, request

def wxinit(signature, timestamp, nonce, echostr):
    temparr = []
    token = "chilema"
    temparr.append(token)
    temparr.append(timestamp)
    temparr.append(nonce)
    temparr.sort()
    newstr = "".join(temparr)
    m = hashlib.sha1()
    m.update(newstr.encode('utf8'))
    sha1str = m.hexdigest()
    if signature == sha1str:
        return echostr
    else:
        return "认证失败，不是微信服务器的请求！"

def getwxid():
    if session.get('opid'):
        return session.get('opid')
    else:
        tokenurl='https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx3bd2eedb7bee8069&secret=07b4bca7c5874366baf960d98dbb1487&code=%s&grant_type=authorization_code' % request.args.get("code")
        op=urllib.request.urlopen(tokenurl).read()
        data = json.loads(op.decode())
        print(data)
        session['opid']=data.get('opid')
        return data.get('opid')


def todict(xml):
    dict={}
    msg = ET.fromstring(xml)
    for child in msg:
        dict[child.tag] = child.text
    return dict

def toxml(dict,url):
    xml='''
<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <ArticleCount>1</ArticleCount>
    <Articles>
    <item>
    <Title><![CDATA[你的成绩帮你查好了]]></Title>
    <Description><![CDATA[学渣慎点哦~]]></Description>
    <PicUrl><![CDATA[]]></PicUrl>
    <Url><![CDATA[%s]]></Url>
    </item>
    </Articles>
</xml>
'''
    return xml % (dict['FromUserName'], dict['ToUserName'], int(time.time()), url)