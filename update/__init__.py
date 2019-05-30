from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.PhantomJS()
client_info_search_url = "https://xclient.info/search/s/"

app_list = ["cleanmymac", "alfred", "betterzip", "beyond compare", "iina", "Navicat Premium", "charles", "DaisyDisk",
            "paw", "Typora"]


class update():
    def execute(self):
        for app_name in app_list:
            # app_name = input("请输入App名称: ")
            driver.get(client_info_search_url + app_name)
            tags = BeautifulSoup(driver.page_source, 'lxml').findAll("div", class_="main")
            for tag in tags:
                name = tag.a["title"]
                if app_name.lower() in name.lower():
                    name_list = name.split(" ")
                    name_list.pop(len(name_list) - 1)
                    name_version = ""
                    for item in name_list:
                        name_version += item
                    href = tag.a["href"] + "#versions"
                    date = tag.find("span", class_="item date").text
                    print(date + " - " + name_version + " - " + href)
        time.sleep(2)


update().execute()
