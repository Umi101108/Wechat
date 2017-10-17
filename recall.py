# coding: utf8
import re
import time
import itchat
from itchat.content import *

msg_information = {}




@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True, isGroupChat=False, isMpChat=False)
def store_msg(msg):
	print msg
	msg_type = msg['Type']
	msg_id = msg['MsgId']
	msg_from = (itchat.search_friends(userName=msg['FromUserName']))['NickName']
	msg_time = msg['CreateTime']
	msg_share_url = None
	if msg_type == 'Text' or msg_type == 'Friends':
		msg_content = msg['Text']
	elif msg_type == 'Attachment' or msg_type == 'Video' or msg_type == 'Picture' or msg_type == 'Recording':
		msg_content = msg['FileName']
		msg['Text'](msg_content)
	elif msg_type == 'Sharing':
		msg_content = msg['Text']
		msg_share_url = msg['Url']
	elif msg_type == 'Card':
		msg_content = msg['RecommendInfo']['NickName'] + u"的名片"
	elif msg_type == 'Map':
		x, y, location = re.search("location x=\"(.*?)\" y=\"(.*?)\".*?label=\"(.*?)\" maptype", msg['OriContent']).group(1, 2, 3)
		msg_content = location if location == '' else u"纬度->{}, 经度->{}".format(x, y)

	msg_information.update({
			msg_id: {
				"msg_from": msg_from,
				"msg_type": msg_type,
				"msg_time": msg_time,
				"msg_content": msg_content,
				"msg_share_url": msg_share_url,
			}
		})

	for k in msg_information.keys():
		if msg_information[k]['msg_time'] < int(time.time())-20:
			del msg_information[k]




@itchat.msg_register(NOTE, isFriendChat=True, isGroupChat=True, isMpChat=True)
def recall(msg):
	if u'撤回了一条消息' in msg['Content']:
		old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
		old_msg = msg_information.get(old_msg_id)

		msg_body = u"{msg_from}撤回了一条{msg_type}消息\n{msg_time}\n{msg_content}".format(
			msg_from=old_msg.get('msg_from'),
			msg_type=old_msg.get('msg_type'),
			msg_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(old_msg.get('msg_time'))),
			msg_content=old_msg.get('msg_content')
			)
		if old_msg.get('msg_type') == 'Sharing':
			msg_body += u"\n链接<{}>".format(old_msg.get('msg_share_url'))
		print msg_body
		itchat.send(msg_body, toUserName='filehelper')

		file = ''
		if old_msg.get('msg_type') == 'Picture':
			file = '@img@%s' % old_msg['msg_content']
		elif old_msg.get('msg_type') == 'Video':
			file = '@vid@%s' % old_msg['msg_content']
		elif old_msg.get('msg_type') == 'Attachment' or old_msg.get('msg_type') == 'Recording':
			file = '@fil@%s' % old_msg['msg_content']

		itchat.send(msg=file, toUserName='filehelper')
		del msg_information[old_msg_id]


itchat.auto_login(hotReload=True, enableCmdQR=2)
itchat.run()
