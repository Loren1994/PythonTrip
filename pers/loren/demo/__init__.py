from selenium import webdriver
from bs4 import BeautifulSoup
import pymysql.cursors
import time
from selenium.webdriver.common.action_chains import ActionChains

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

driver = webdriver.PhantomJS()


class Demo():
    __isLoop = 1

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
        driver.get(web_url)
        self.getNextPage()
        tags = BeautifulSoup(driver.page_source, 'lxml').find_all('li', class_='slide-item')
        item_tags = BeautifulSoup(driver.page_source, 'lxml').find_all('div', class_='bui-box single-mode')
        # 列表数据
        itemList = []
        for itemTag in item_tags:
            k = itemTag.find('div', class_='bui-left single-mode-lbox').a['href'].split('/')[2]
            u = itemTag.find('div', class_='bui-left single-mode-lbox').a.img['src']
            t = itemTag.find('div', class_='single-mode-rbox').find('span', class_='footer-bar-action')
            # item = ()
            # itemList.append(item)
            print(k + "\n" + u)
            print(t)
        # 轮播图数据
        list = []
        for tag in tags:
            t = tag.a.p.text
            u = tag.a.img['src']
            k = tag.a['href']
            key = k.split('/')[2]
            timeStr = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            # 0:轮播图
            item = (t, u, key, timeStr, 0)
            list.append(item)
        self.isExist(self, list)

    # 所有当天数据
    def getNextPage(self):
        # 由于图片是懒加载，所以必须滚动一遍到底部才可以拿到图片URL display:none的元素拿到的位置是(0,0)
        # 滚动到底部三种方式
        # 1、driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 2、actions = ActionChains(driver)
        # actions.move_to_element(e).perform()
        if self.__isLoop == 0:
            return
        elems = driver.find_elements_by_class_name("lazy-load-img")
        driver.execute_script("arguments[0].scrollIntoView();", elems[len(elems) - 1])
        time.sleep(3)
        item_tags = BeautifulSoup(driver.page_source, 'lxml').find_all('div', class_='bui-box single-mode')
        for itemTag in item_tags:
            # k = itemTag.find('div', class_='bui-left single-mode-lbox').a['href'].split('/')[2]
            # i = itemTag.find('div', class_='bui-left single-mode-lbox').a.img['src']
            u = itemTag.find('div', class_='single-mode-rbox').find('span', class_='footer-bar-action')
            if u.text == ' 1天前':
                print("超过一天")
                self.__isLoop = 0
                print(len(elems))
                for e in elems:
                    driver.execute_script("arguments[0].scrollIntoView();", e)
                    time.sleep(0.5)
                print("遍历结束")
                break
        self.getNextPage()

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
# 需要connection.close()
# 需要driver.close()
