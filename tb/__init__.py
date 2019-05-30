# -*- coding=UTF-8 -*-
from selenium import webdriver
import time
import datetime
from tkinter import *
import threading
import tkinter.messagebox
from selenium.webdriver.support.wait import WebDriverWait


def make_app():
    app = Tk()
    app.geometry('300x150')
    Label().pack()
    Label(text='请务必按照格式输入抢单时间').pack()
    # Label(text='2019-02-27 12:49:10.88').pack()
    e_time = Entry(name='ipt')
    e_time.insert(10, "2019-04-04 17:31:00.0000")
    e_time.pack()
    # Label(name='lb1', text='抢单中').pack()
    Button(text='点击开始抢单', command=login).pack()
    return app


def login():
    th = threading.Thread(target=sign_up)
    th.start()


def sign_up():
    options = webdriver.ChromeOptions()
    # 不加载图片,加快访问速度
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # 设置为开发者模式，避免被识别
    options.add_experimental_option('excludeSwitches',
                                    ['enable-automation'])
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://www.taobao.com/')
    time.sleep(1)
    if driver.find_element_by_link_text('亲，请登录'):
        driver.find_element_by_link_text('亲，请登录').click()
        # tkinter.messagebox.showinfo('提示', '请在10秒内完成登录二维码扫描')
        time.sleep(10)
        driver.get("https://cart.taobao.com/cart.htm")
        # while tkinter.messagebox.askokcancel('提示', '请选择抢购的商品。打勾后点击确定') == False:
        #     tkinter.messagebox.askokcancel('提示', '请选择抢购的商品。打勾后点击确定')
        # tkinter.messagebox.showinfo('提示', '请勿关闭网页')

        while True:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            if now >= app.children['ipt'].get():
                print("时间到!" + now)
                try:
                    time.sleep(0.1)
                    driver.find_element_by_link_text('结 算').click()
                    print("进入确认订单页面" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
                    time.sleep(0.1)
                    confirm_window = driver.current_window_handle
                    print("driver刷新完:" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
                    # while True:
                    #     if driver.find_element_by_link_text('提交订单'):
                    #         driver.find_element_by_link_text('提交订单').click()
                    #     time.sleep(0.01)

                    # 使用selenium提供的WebDriverWait方法，每poll_frequency秒检查一次定位的元素，超时设置是2秒
                    WebDriverWait(driver, timeout=2, poll_frequency=0.1).until(
                        lambda driver: driver.find_element_by_link_text('提交订单'))
                    driver.find_element_by_link_text('提交订单').click()
                except:
                    time.sleep(0.001)
                break
            else:
                time.sleep(0.001)


if __name__ == '__main__':
    app = make_app()
    app.mainloop()
