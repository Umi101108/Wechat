# coding: utf8

import re
import itchat
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image


signature_list = []

itchat.auto_login(hotReload=True, enableCmdQR=2)
friends = itchat.get_friends(update=True)[0:]
for i in friends:
    signature = re.sub(r'<.*?>', '', i["Signature"]).replace(' ', '').replace('\n', '')
    print signature
    signature_list.append(signature)

text = "".join(signature_list)

wordlist_after_jieba = jieba.cut(text, cut_all=True)
word_space_split = " ".join(wordlist_after_jieba)
abel_mask = np.array(Image.open('wechat.jpg'))
my_wordcloud = WordCloud(background_color="white",
                         max_words=200,
                         max_font_size=40,
                         random_state=42,
                         font_path='./DroidSansFallbackFull.ttf',
                         mask=abel_mask
                         ).generate(word_space_split)

plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()