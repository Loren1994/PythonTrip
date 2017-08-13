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
home_insert_sql = "INSERT INTO `tt_home_page` (`content`, `pic_url`,`click_key`,`create_time`,`type`) VALUES (%s,%s,%s,%s,%s)"
home_select_sql = "SELECT `*` FROM `tt_home_page` WHERE `click_key`=%s"
home_update_sql = "UPDATE tt_home_page SET content = %s, pic_url = %s WHERE click_key = %s"


class Demo():
    @staticmethod
    def db_operate(sql, item):
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, item)

            connection.commit()
        finally:
            # 全局connection，不能直接close
            # connection.close()
            print('db_operate finally')

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
            # 0:轮播图 1:首页列表
            item = (t, u, key, timeStr, 0)
            list.append(item)
        self.isExist(self, list)

    # insert or update
    @staticmethod
    def isExist(self, list):
        try:
            with connection.cursor() as cursor:
                for item in list:
                    key = item[2]
                    cursor.execute(home_select_sql, (key))
                    result = cursor.fetchone()
                    if result == None:
                        self.db_operate(home_insert_sql, item)
                    else:
                        temp = (item[0], item[1], item[2])
                        self.db_operate(home_update_sql, temp)
        finally:
            connection.close()
            print('isExist finally')


demo = Demo()
demo.get_data()
# connection.close()
