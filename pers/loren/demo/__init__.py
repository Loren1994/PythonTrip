from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import os
import time
import pymysql.cursors


class Demo():
    web_url = 'http://www.toutiao.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

    @staticmethod
    def db_operate(sql, list):
        connection = pymysql.connect(host='localhost',
                                     port=3306,
                                     user='root',
                                     password='root',
                                     db='coder_hub',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                cursor.executemany(sql, list)

            connection.commit()
        finally:
            connection.close()

    def get_pic(self):
        print("<<<<<<<<getting content>>>>>>>>")
        driver = webdriver.PhantomJS()
        driver.get(self.web_url)
        tags = BeautifulSoup(driver.page_source, 'lxml').find_all('li', class_='slide-item')

        list = []
        for tag in tags:
            t = tag.a.p.text
            u = tag.a.img['src']
            k = tag.a['href']
            print(t)
            print(u)
            print(k)
            item = (t, u)
            list.append(item)
        # sql = "INSERT INTO `tt_home_page` (`content`, `pic_url`) VALUES (%s,%s)"
        # self.db_operate(sql, list)


demo = Demo()
demo.get_pic()
