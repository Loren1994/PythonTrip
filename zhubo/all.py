from functools import reduce
from json import JSONDecodeError

import requests

platform_url = "http://api.vipmisss.com:81/xcdsw/json.txt"
base_url = "http://api.vipmisss.com:81/xcdsw/"


class All:

    def __init__(self):
        self.__results = []

    def exec(self):
        self.fetch_urls()

    def fetch_urls(self):
        temp = []
        for it in requests.get(platform_url).json()["pingtai"]:
            url = base_url + it["address"]
            print(url)
            try:
                json = requests.get(url).json()
                temp.extend(json["zhubo"])
            except JSONDecodeError:
                print("invalid")
        self.__results = reduce(lambda x, y: x if y in x else x + [y], [[], ] + temp)
        print(len(self.__results))
        self.filter()

    def filter(self):
        while True:
            key = input("input key: ")
            if not key:
                continue
            if key == "~":
                break
            for it in self.__results:
                if key in it["title"]:
                    print("%s   %s" % (it["address"], it["title"]))
        self.fetch_urls()


if __name__ == "__main__":
    All().exec()
