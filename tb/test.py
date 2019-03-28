# -*- coding=UTF-8 -*-
from selenium import webdriver
import time
import datetime
from tkinter import *
import threading
import tkinter.messagebox

f = open("out.txt", "w+")

def make_app():
    app = Tk()
    app.geometry('300x250')
    Label().pack()
    Label(text='请务必按照格式输入抢单时间').pack()
    # Label(text='2019-02-27 12:49:10.88').pack()
    e_time = Entry(name='ipt',text='2019-02-27 12:49:10.88')
    e_time.insert(10,"2019-02-27 14:19:00.00")
    e_time.pack()
    # Label(text='请输入买家备注(如不填写可提高抢单速度)').pack()
    # Entry(name='ipt2').pack()
    Label(name='lb1', text='抢单中').pack()
    b=tkinter.Button(text='点击开始抢单', command=login)
    b.pack()
    return app

def login():
    th = threading.Thread(target=sign_up)
    th.start()

def sign_up():
    driver = webdriver.Chrome()
    driver.get('https://www.taobao.com/')
    time.sleep(1)
    if driver.find_element_by_link_text('亲，请登录'):
        driver.find_element_by_link_text('亲，请登录').click()
        # tkinter.messagebox.showinfo('提示', '请在15秒内完成登录二维码扫描')
        time.sleep(10)
        driver.get("https://cart.taobao.com/cart.htm")
        # while tkinter.messagebox.askokcancel('提示', '请选择抢购的商品。打勾后点击确定') == False:
        #     tkinter.messagebox.askokcancel('提示', '请选择抢购的商品。打勾后点击确定')
        # tkinter.messagebox.showinfo('提示', '请勿关闭网页')
        # 无买家留言
        if app.children['ipt2'].get() == '':
             while True:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                if now >= app.children['ipt'].get():
                    try:
                        if app.children['lb1']['text'] == '抢单中':
                            if driver.find_element_by_id('J_Go'):
                                driver.find_element_by_id('J_Go').click()
                                app.children['lb1']['text'] = '商品上线'
                        if app.children['lb1']['text'] != '抢单中':
                            driver.find_element_by_link_text('结算').click()
                            # 进入确认订单页面
                            # 刷新driver
                            time.sleep(0.1)
                            confirm_window = driver.current_window_handle
                            print(confirm_window.text, f)
                            confirm = driver.find_element_by_link_text('提交订单')
                            print(confirm.text, f)
                            # time.sleep(0.1)
                            confirm.click()
                            # tkinter.messagebox.showinfo('提示', '抢单成功')
                    except:
                        time.sleep(0.001)
                time.sleep(0.001)
        # 有买家留言
        else:
            while True:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                if now >= app.children['ipt'].get():
                    try:
                        if app.children['lb1']['text'] == '抢单中':
                            if driver.find_element_by_id('J_Go'):
                                driver.find_element_by_id('J_Go').click()
                                app.children['lb1']['text'] = '商品上线'
                        if app.children['lb1']['text'] != '抢单中':
                            input_text = driver.find_elements_by_tag_name('textarea')[0]
                            if input_text:
                                text = app.children['ipt2'].get()
                                input_text.send_keys(text)
                                driver.find_element_by_link_text('结算').click()
                                tkinter.messagebox.showinfo('提示', '抢单成功')
                    except:
                        time.sleep(0.001)
                time.sleep(0.001)

if __name__ == '__main__':
    app = make_app()
    app.mainloop()

