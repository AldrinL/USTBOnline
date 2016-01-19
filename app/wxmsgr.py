import time
import xml.etree.ElementTree as ET
import sys
import hashlib

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