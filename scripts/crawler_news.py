#!/usr/bin/python
# encoding:utf-8
 
import json, urllib.request

from bs4 import BeautifulSoup

from news.models import News
from tags.models import Tag


def run(*args):
    data = {}
    data["appkey"] = "055412fc5fee23e4"
    data["channel"] = args[0]  #新闻频道(头条,财经,体育,娱乐,军事,教育,科技,NBA,股票,星座,女性,健康,育儿)
    data["num"] = 40
    for i in range(0, 200, 40):
        data["num"] = 40
        data['start'] = i
        url_values = urllib.parse.urlencode(data)
        url = "https://api.jisuapi.com/news/get" + "?" + url_values
        result = urllib.request.urlopen(url)
        jsonarr = json.loads(result.read())

        if jsonarr["status"] != 0:
            print(jsonarr["msg"])
            exit()
        result = jsonarr["result"]
        
        print(result["channel"],result["num"])
        tag = Tag.objects.filter(name=data["channel"])
        for val in result["list"]:
            new = News
            soup = BeautifulSoup(val['content'], "html.parser")
            imgs = soup.select('img')
            img = None
            if len(imgs) > 0:
                img = imgs[0].get('src')
            content = '![](%s)\n%s' % (img, soup.get_text())
            news = News.objects.create(title=val["title"], content=content, cover_image=img)
            news.tags.set(tag)