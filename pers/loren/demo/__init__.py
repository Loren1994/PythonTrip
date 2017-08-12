from selenium import webdriver
from bs4 import BeautifulSoup
import pymysql.cursors
import time

connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='root',
                             db='coder_hub',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
web_url = 'http://www.toutiao.com/'


class Demo():
    @staticmethod
    def db_operate(sql, list):
        try:
            with connection.cursor() as cursor:
                cursor.executemany(sql, list)

            connection.commit()
        finally:
            connection.close()

    def get_data(self):
        print("<<<<<<<<getting content>>>>>>>>")
        driver = webdriver.PhantomJS()
        driver.get(web_url)
        tags = BeautifulSoup(driver.page_source, 'lxml').find_all('li', class_='slide-item')

        list = []
        for tag in tags:
            t = tag.a.p.text
            u = tag.a.img['src']
            k = tag.a['href']
            key = k.split('/')[2]
            timeStr = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            print(t)
            print(u)
            print(key)
            print(timeStr)
            # 0:??? 1:????
            item = (t, u, key, timeStr,0)
            list.append(item)

        sql = "INSERT INTO `tt_home_page` (`content`, `pic_url`,`click_key`,`create_time`,`type`) VALUES (%s,%s,%s,%s,%s)"
        self.db_operate(sql, list)

    # ??key????????insert or update
    # def isExist(list):


demo = Demo()
demo.get_data()
