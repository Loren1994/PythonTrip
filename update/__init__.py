from selenium import webdriver
from bs4 import BeautifulSoup
import time

headers = {
    'Host': 'xclient.info',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Accept-Language': 'en-us',
    'Accept-Encoding': 'gzip, deflate',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Mobile Safari/537.36',
    'Cookie': 'PHPSESSID=6vasofbgvm907nqedn9ntdlu8u; Hm_lvt_befb95b3cbb10a937d15e5181625c9f2=1559196880; Hm_lpvt_befb95b3cbb10a937d15e5181625c9f2=1559196880; _ga=GA1.2.2045038734.1559196881; _gid=GA1.2.1046198329.1559196881; _gat_gtag_UA_137913203_1=1'}

cap = webdriver.DesiredCapabilities.PHANTOMJS
cap["phantomjs.page.customHeaders.Cookie"] = headers['Cookie']
driver = webdriver.PhantomJS(desired_capabilities=cap)

client_info_search_url = "https://xclient.info/search/s/"
# app_name = "cleanmymac"


class update():
    def execute(self):
        app_name = input("请输入App名称: ")
        driver.get(client_info_search_url + app_name)
        tags = BeautifulSoup(driver.page_source, 'lxml').findAll("div", class_="main")
        for tag in tags:
            name = tag.a["title"]
            if app_name.lower() in name.lower():
                name_version = name.split(" ")[0] + name.split(" ")[1]
                href = tag.a["href"]
                date = tag.find("span", class_="item date").text
                print(date + " - " + name_version + " - " + href)


update().execute()
