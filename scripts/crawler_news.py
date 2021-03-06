#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import json, urllib.request

from bs4 import BeautifulSoup

from news.models import News
from tags.models import Tag


def run(*args):
    data = {}
    arg_list = args[0].split(',')
    data["appkey"] = "d952cc6f7f38503b"
    print('目标爬取 ' + arg_list[0].encode('utf-8').decode() + ' 分类下的 ' + arg_list[1].encode('utf-8').decode() +' 条新闻...')
    tag = Tag.objects.get(unique_name=arg_list[0])
    print('正在爬取 ' + tag.name.encode('utf-8').decode() +' 分类下的新闻.......')
    count = 0
    data["channel"] = tag.name #新闻频道(头条,财经,体育,娱乐,军事,教育,科技,NBA,股票,星座,女性,健康,育儿)
    data["num"] = min(int(arg_list[1]),40)

    # url_values = urllib.parse.urlencode(data)
    # url = "https://api.jisuapi.com/news/get" + "?" + url_values
    # result = urllib.request.urlopen(url)
    # jsonarr = json.loads(result.read().decode(), encoding="utf-8")
    # print(jsonarr)

    for i in range(0, int(arg_list[1]), 40):
        data['start'] = i
        url_values = urllib.parse.urlencode(data)
        url = "https://api.jisuapi.com/news/get" + "?" + url_values
        result = urllib.request.urlopen(url)
        jsonarr = json.loads(result.read().decode(), encoding="utf-8")
        if jsonarr["status"] != 0:
            print(jsonarr["msg"])
            exit()
        result = jsonarr["result"]
        
        # print(result["channel"],result["num"])
        tag = Tag.objects.filter(name=data["channel"])
        for val in result["list"]:
            new = News
            soup = BeautifulSoup(val['content'], "html.parser")
            imgs = soup.select('img')
            img = None
            if len(imgs) > 0:
                img = imgs[0].get('src')
            else: 
                continue
            content = '![](%s)\n%s' % (img, soup.get_text())
            news = News.objects.create(title=val["title"], content=content, cover_image=img)
            news.tags.set(tag)
            count += 1
    
    print('成功爬取符合条件的 ' + str(count) + ' 条新闻。')