# coding: utf8
import re
import time
import itchat
from itchat.content import *

@itchat.msg_register([TEXT, NOTE], isFriendChat=True)
def red_envelope(msg):
    print msg
    if u'收到红包' in msg['Content']:
        msg_from = (itchat.search_friends(userName=msg['FromUserName']))['NickName']
        msg_body = u"{}给你发了一个红包".format(msg_from)
        itchat.send(msg_body, toUserName='filehelper')

itchat.auto_login(hotReload=True, enableCmdQR=2)
itchat.run()
