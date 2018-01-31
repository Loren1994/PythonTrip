# -*- coding:utf-8 -*-
import codecs
import re

import jieba.analyse
import matplotlib.pyplot as plt
import requests
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator
from os import path

d = path.dirname(__file__)

# 填入准确的微博昵称即可生成词图
input_nick_name = "GAI周延"

container_id = ""
uid = ""
total_count = 0

url = "https://m.weibo.cn/api/container/getIndex"
search_url = "https://m.weibo.cn/searchs/result"

search_headers = {
    "Host": "m.weibo.cn",
    "Referer": "https://m.weibo.cn/searchs",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.85 Mobile Safari/537.36",
}
headers = {
    "Host": "m.weibo.cn",
    "Referer": "https://m.weibo.cn/u/" + uid,
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1",
}

search_params = {
    "type": "user",
    "queryVal": input_nick_name
}
user_result_params = {
    "type": "user",
    "queryVal": input_nick_name,
    "lfid": "0",
    "containerid": "{container_id}"
}
params = {
    "type": "uid",
    "value": "{uid}",
    "containerid": "{containerid}",
    "page": "{page}"}


def get_user_ids():
    res = requests.get(search_url, params=search_params, headers=search_headers)
    cookie = res.headers.get("Set-Cookie")
    try:
        temp = cookie.split("%3D")[1]
        global container_id
        container_id = temp.split("%26")[0]
    except:
        print("分割containerid发生异常!!!")
    else:
        print("containerid=" + container_id)


def get_user_info():
    user_result_params['containerid'] = container_id
    user_res = requests.get(url, user_result_params)
    user = user_res.json().get("data").get("cards")[1].get("card_group")[0].get("user")
    global uid
    uid = str(user.get("id"))
    global total_count
    total_count = user.get("statuses_count")
    print("微博数量:" + str(total_count) + " uid=" + uid)


def fetch_data():
    page = 1
    blogs = []
    size = (total_count // 10) + 2
    for i in range(0, size):
        params['value'] = uid
        params['containerid'] = "107603" + uid
        params['page'] = str(page)
        res = requests.get(url, params=params, headers=headers)
        cards = res.json().get("data").get("cards")

        for card in cards:
            # 每条微博的正文内容
            if card.get("card_type") == 9:
                text = card.get("mblog").get("text")
                text = clean_html(text)
                blogs.append(text)
        page += 1
        print("抓取第{page}页，目前总共抓取了 {count} 条微博".format(page=page, count=len(blogs)))
        with codecs.open('weibo1.txt', 'w', encoding='utf-8') as f:
            f.write("\n".join(blogs))


def generate_image():
    data = []
    jieba.analyse.set_stop_words("./stopwords.txt")

    with codecs.open("weibo1.txt", 'r', encoding="utf-8") as f:
        for text in f.readlines():
            data.extend(jieba.analyse.extract_tags(text, topK=20))
        data = " ".join(data)
        # mask_img = imread('./52f90c9a5131c.jpg', flatten=True)
        mask_img = imread(path.join(d, "./ic_mask.png"))
        wordcloud = WordCloud(
            font_path='/Users/loren/PycharmProjects/crawler_html2pdf/DroidSansFallback.ttf',
            background_color='white',
            mask=mask_img,
            max_words=2000,
            max_font_size=100,
            random_state=42
        )
        wordcloud.generate(data)
        image_colors = ImageColorGenerator(mask_img)
        plt.figure()
        # 显示图片
        plt.imshow(wordcloud.recolor(color_func=image_colors))
        plt.axis("off")
        plt.show()
        wordcloud.to_file(path.join(d, "world_cloud.png"))
        # 直接保存
        # plt.imshow(wordcloud.recolor(color_func=image_colors))
        # plt.axis('off')
        # plt.savefig('./heart2.jpg')


def clean_html(raw_html):
    pattern = re.compile(r'<.*?>|转发微博|//:|Repost|，|？|。|、|分享图片|回复@.*?:|//@.*')
    text = re.sub(pattern, '', raw_html)
    return text


if __name__ == '__main__':
    get_user_ids()
    get_user_info()
    fetch_data()
    generate_image()
