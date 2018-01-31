import selenium.webdriver
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

home_insert_sql = "INSERT INTO `tt_home_page` (`content`, `pic_url`,`click_key`,`create_time`,`type`) VALUES (%s,%s,%s,%s,%s)"
home_select_sql = "SELECT `*` FROM `tt_home_page` WHERE `click_key`=%s"
home_update_sql = "UPDATE tt_home_page SET content = %s, pic_url = %s WHERE click_key = %s"

list_insert_sql = "INSERT INTO `tt_home_list` (`content`, `pic_url`,`click_key`,`create_time`,`type`,`web_time`,`author_name`,`author_head`,`comment_num`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
list_select_sql = "SELECT `*` FROM `tt_home_list` WHERE `click_key`=%s"
list_update_sql = "UPDATE tt_home_list SET content = %s, pic_url = %s, web_time = %s, comment_num = %s WHERE click_key = %s"

headers = {
    'Host': 'www.toutiao.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Accept-Language': 'en-us',
    'Accept-Encoding': 'gzip, deflate',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
    'Cookie': 'tt_webid=6496247174204114445; __tasessionId=jb4b94add1517377040502; CNZZDATA1259612802=1731481297-1512525102-%7C1517373434; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6496247174204114445; _ga=GA1.2.881746538.1517377022; _gid=GA1.2.302154837.1517377022; UM_distinctid=160298a34d9461-064e109cf061bb-1c451b26-13c680-160298a34da6eb'}
web_url = 'https://www.toutiao.com/'
# 设置header
cap = webdriver.DesiredCapabilities.PHANTOMJS
cap["phantomjs.page.settings.userAgent"] = headers['User-Agent']  # 设置请求header头信息
# cap["phantomjs.page.settings.loadImages"] = False  # 禁止加载图片
cap["phantomjs.page.customHeaders.Host"] = headers['Host']
cap["phantomjs.page.customHeaders.Cookie"]=headers['Cookie']
driver = webdriver.PhantomJS(desired_capabilities=cap)


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
        print(">>>>>>>>getting content<<<<<<<<")
        driver.get(web_url)
        self.getNextPage()
        tags = BeautifulSoup(driver.page_source, 'lxml').find_all('li', class_='slide-item')
        item_tags = BeautifulSoup(driver.page_source, 'lxml').find_all('div', class_='bui-box single-mode')
        # 列表数据
        itemList = []
        for itemTag in item_tags:
            # key
            k = itemTag.find('div', class_='bui-left single-mode-lbox').a['href'].split('/')[2]
            # 图片
            u = itemTag.find('div', class_='bui-left single-mode-lbox').a.img['src']
            # 时间
            t = itemTag.find('div', class_='single-mode-rbox').find('span', class_='footer-bar-action').text
            # 标题
            title = itemTag.find('div', class_='title-box').a.text
            # 分类
            type = itemTag.find('div', class_='bui-left footer-bar-left').a.text
            # 作者头像
            # head = itemTag.find('div', class_='single-mode-rbox').find('a', class_='footer-bar-action media-avatar')
            # 作者昵称
            name = itemTag.find('div', class_='bui-left footer-bar-left').find_all('a',
                                                                                   class_='footer-bar-action source')
            na = "" if len(name) == 0 else name[0].text
            # 评论数
            num = itemTag.find('div', class_='bui-left footer-bar-left').find_all('a',
                                                                                  class_='footer-bar-action source')
            nu = "" if len(num) <= 1 else num[1].text
            createTime = int(time.time())
            if '//' in u:
                item = (title, u.split('//')[1], k, createTime, type, t, na, 'head', nu)
                itemList.append(item)
            print(k + "\n" + u + t + "\n" + title + "\n" + type + na + nu)
        self.isExistList(self, itemList)
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
        # 由于图片是懒加载，所以必须滚动一遍到底部才可以拿到图片URL 否则是svg+xml的Base64
        # display:none的元素拿到的位置是(0,0)
        # 滚动到底部三种方式
        # 1、driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 2、actions = ActionChains(driver)
        # actions.move_to_element(e).perform()
        if self.__isLoop == 0:
            return
        time.sleep(3)
        print(driver.page_source)
        elems = driver.find_elements_by_class_name('lazy-load-img')
        # elems = driver.find_elements_by_xpath("//img[@lazy='loaded']")
        print(len(elems))
        # driver.execute_script("arguments[0].scrollIntoView();", elems[len(elems) - 1])
        time.sleep(3)
        item_tags = BeautifulSoup(driver.page_source, 'lxml').find_all('div', class_='bui-box single-mode')
        for itemTag in item_tags:
            u = itemTag.find('div', class_='single-mode-rbox').find('span', class_='footer-bar-action')
            if u.text == ' 1天前':
                print("超过一天")
                self.__isLoop = 0
                print(len(elems))
                for e in elems:
                    driver.execute_script("arguments[0].scrollIntoView();", e)
                    time.sleep(0.8)
                # for h in elems_head:
                #     driver.execute_script("arguments[0].scrollIntoView();", h)
                #     time.sleep(0.5)
                print("遍历结束")
                break
        self.getNextPage()

    # home insert or update
    @staticmethod
    def isExist(self, list):
        try:
            with connection.cursor() as cursor:
                for item in list:
                    key = item[2]
                    cursor.execute(home_select_sql, (key))
                    result = cursor.fetchone()
                    if result is None:
                        self.db_operate(home_insert_sql, item)
                    else:
                        temp = (item[0], item[1], item[2])
                        self.db_operate(home_update_sql, temp)
        finally:
            connection.close()
            print('isExist finally')

    # list insert or update
    @staticmethod
    def isExistList(self, list):
        try:
            with connection.cursor() as cursor:
                for item in list:
                    key = item[2]
                    cursor.execute(list_select_sql, (key))
                    result = cursor.fetchone()
                    if result is None:
                        self.db_operate(list_insert_sql, item)
                    else:
                        temp = (item[0], item[1], item[5], item[8], item[2])
                        self.db_operate(list_update_sql, temp)
        finally:
            # connection.close()
            print('isExistList finally')


demo = Demo()
demo.get_data()
# 需要connection.close()
# 需要driver.close()
