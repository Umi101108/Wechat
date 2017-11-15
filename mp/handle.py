# coding: utf8
# fielname: handle.py

import hashlib
import reply
import receive
from tuling import Tuling
from cbooo import Cbooo
from how_old import How_old
import web

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data)==0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "umi101108"

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is \n", webData # 后台打印日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.EventMsg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.Event == 'subscribe':
                    content = '你好，这个公众号还未开化哦'
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
            elif isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    print recMsg.Content
                    content = Tuling(recMsg.Content).reply().encode('utf8')
                    print content
                    if recMsg.Content == '智障':
                        content = '666'
                    elif recMsg.Content == '我是智障':
                        title = '中秋快乐'
                        description = '惊不惊喜'
                        picUrl = 'http://pic33.nipic.com/20130923/11927319_180343313383_2.jpg'
                        url = 'http://www.umi101108.com'
                        replyMsg = reply.TextImageMsg(toUser, fromUser, title, description, picUrl, url)
                        return replyMsg.send()
                    elif recMsg.Content == '电影':
                        piaofang = Cbooo().getPiaofang()
                        replyMsg = reply.MultiTextImageMsg(toUser, fromUser, piaofang, 5)
                        return replyMsg.send()
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                elif recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    PicUrl = recMsg.PicUrl
                    try:
                        content = How_old().getAttributes(PicUrl)
                        print content
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                    except:
                        replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                else:
                    return reply.Msg().send()
            else:
                print "暂且不处理"
                return reply.Msg().send()
        except Exception, Argument:
            return Argument
