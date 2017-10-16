# coding: utf8
# filename: tuling.py

import requests

class Tuling(object):
    def __init__(self, info):
        self.apiUrl = 'http://www.tuling123.com/openapi/api'
        self.key = '3cacc71cd81b435ab94de308eb825baa'
        self.info = info

    def reply(self):
        data = {
            'key': self.key,
            'info': self.info,
            'userid': 'wechat-rebot',
        }
        r = requests.post(self.apiUrl, data=data).json().get('text')
        return r

if __name__ == "__main__":
    info = '今天是什么日子'
    tuling = Tuling(info)
    print tuling.reply()
