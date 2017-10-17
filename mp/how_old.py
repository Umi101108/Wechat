# coding: utf8
# filename: how_old.py
import requests
import re

class How_old(object):
    def __init__(self):
        self.url = 'https://how-old.net/Home/Analyze?isTest=False&source=&version=how-old.net'

    def getAttributes(self, picUrl):
        data = {'data': requests.get(picUrl).content}
        response = requests.post(self.url, files=data)
        print response
        attributes = re.search(r'gender\\":\\"(.*?)\\",\\"age\\":(.*?),', response.content)
        gender = attributes.group(1)
        age = attributes.group(2)
        if gender == 'Female':
            content = '图中人物为女性'
        elif gender == 'Male':
            content = '图中人物为男性'
        else:
            content = '图中人物性别未知'
        content += '，年龄：' + age + '岁'
        return content
