# coding: utf-8
# filename: cbooo.py
import time
import requests
import json

class Cbooo(object):
    def __init__(self):
        self.cbooo_url = 'http://www.cbooo.cn/BoxOffice/GetHourBoxOffice?d={}'
        self.img_url = 'http://www.cbooo.cn/moviepic/'
        self.item_url = 'http://www.cbooo.cn/m/'
        self.piaofang = {}

    def getPiaofang(self):
        url = self.cbooo_url.format(int(time.time()*1000))
        response = requests.get(url)
        movies = json.loads(response.content)['data2']
        i = 0
        for movie in movies:
            movie_name = movie['MovieName']
            movie_box = movie['sumBoxOffice']
            movie_img = self.img_url + movie['MovieImg']
            movie_url = self.item_url + movie['mId']
            self.piaofang[i] = {
                'title': movie_name + u' 票房：' + u"%.2f亿"%(float(movie_box)/10000.0),
                'description': '233',
                'picUrl': movie_img,
                'url': movie_url,
            }
            i += 1
        print self.piaofang
        return self.piaofang


if __name__ == '__main__':
    cbooo = Cbooo()
    piaofang = cbooo.getPiaofang()
    for k, v in piaofang.iteritems():
        print k, v
