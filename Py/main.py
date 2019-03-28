# -*- coding: utf-8 -*-
import WeChat
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import re
from time import sleep
from bs4 import BeautifulSoup
import requests
import json
import urllib.parse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from math import ceil
import threading
import inspect
import ctypes
import random



class MyMainWindow(WeChat.Ui_MainWindow):
    def __init__(self):
        self.sess = requests.Session()
        self.headers = {
            'Host': 'mp.weixin.qq.com',
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
        }
        self.rootpath = os.getcwd() + r"/spider/"  # 全局变量，存放路径
        self.time_gap = 10  # 全局变量，每页爬取等待时间
        self.thread_list = []

    def setupUi(self, MainWindow):
        super(MyMainWindow, self).setupUi(MainWindow)

    def Start_Run(self):
        Process_thread = threading.Thread(target=self.Process, daemon=True)
        Process_thread.start()
        self.thread_list.append(Process_thread)

    def Stop_Run(self):
        try:
            self.stop_thread(self.thread_list.pop())
            self.label_notes.setText("终止成功!")
        except Exception as e:
            print(e)

    def Process(self):
        query_name = self.LineEdit_target.text()  # 公众号的英文名称
        username = self.LineEdit_user.text()  # 自己公众号的账号
        pwd = self.LineEdit_pwd.text()  # 自己公众号的密码
        self.time_gap = self.LineEdit_timegap.text()  # 每页爬取等待时间")
        if (self.time_gap == ""):
            self.time_gap = 10
        else:
            self.time_gap = int(self.time_gap)
        [token, cookies] = self.Login(username, pwd)
        self.Add_Cookies(cookies)
        [fakeid, nickname] = self.Get_WeChat_Subscription(token, query_name)
        self.rootpath = os.getcwd() + r"/spider/" + nickname
        os.makedirs(self.rootpath)
        self.Get_Articles(token, fakeid)

    def Login(self, username, pwd):
        self.label_notes.setText("正在打开浏览器,请稍等")
        browser = webdriver.Firefox()
        # browser = webdriver.Chrome()
        browser.maximize_window()

        browser.get(r'https://mp.weixin.qq.com')
        browser.implicitly_wait(60)
        account = browser.find_element_by_name("account")
        password = browser.find_element_by_name("password")
        if (username != "" and pwd != ""):
            account.click()
            account.send_keys(username)
            password.click()
            password.send_keys(pwd)
            browser.find_element_by_xpath(r'//*[@id="header"]/div[2]/div/div/form/div[4]/a').click()
        else:
            self.label_notes.setText("* 请在10分钟内手动完成登录 *")
        WebDriverWait(browser, 60 * 10, 0.5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, r'.weui-desktop-account__nickname'))
        )
        self.label_notes.setText("登陆成功")
        token = re.search(r'token=(.*)', browser.current_url).group(1)
        cookies = browser.get_cookies()
        with open("cookie.json", 'w+') as fp:
            fp.write(json.dumps(cookies))
            self.label_notes.setText(">> 本地保存cookie")
            fp.write(json.dumps([{"token": token}]))
            self.label_notes.setText(">> 本地保存token")
            fp.close()
        browser.close()
        # print('token:', token)
        return token, cookies

    def Add_Cookies(self, cookie):
        c = requests.cookies.RequestsCookieJar()
        for i in cookie:  # 添加cookie到CookieJar
            c.set(i["name"], i["value"])
            self.sess.cookies.update(c)  # 更新session里的cookie

    def Get_WeChat_Subscription(self, token, query):
        if (query == ""):
            query = "xinhuashefabu1"
        url = r'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={0}&lang=zh_CN&f=json&ajax=1&random=0.5182749224035845&query={1}&begin=0&count=5'.format(
            token, query)
        html_json = self.sess.get(url, headers=self.headers).json()
        # print(html_json)
        fakeid = html_json['list'][0]['fakeid']
        nickname = html_json['list'][0]['nickname']
        # print("fakeid:", fakeid)
        self.label_notes.setText("nickname: "+nickname)
        return fakeid, nickname

    def Get_Articles(self, token, fakeid):
        title_buf = []
        link_buf = []
        img_buf = []

        Total_buf = []
        url = r'https://mp.weixin.qq.com/cgi-bin/appmsg?token={0}&lang=zh_CN&f=json&ajax=1&random={1}&action=list_ex&begin=0&count=5&query=&fakeid={2}&type=9'.format(token,  random.uniform(0, 1), fakeid)
        html_json = self.sess.get(url, headers=self.headers).json()
        try:
            Total_Page = ceil(int(html_json['app_msg_cnt']) / 5)
        except Exception as e:
            self.label_notes.setText("!! 失败信息："+html_json['base_resp']['err_msg'])
            return
        table_index = 0
        for i in range(Total_Page):
            self.label_notes.setText("第[%d/%d]页" % (i + 1, Total_Page))
            print("第[%d/%d]页" % (i + 1, Total_Page))
            begin = i * 5
            url = r'https://mp.weixin.qq.com/cgi-bin/appmsg?token={0}&lang=zh_CN&f=json&ajax=1&random={1}&action=list_ex&begin={2}&count=5&query=&fakeid={3}&type=9'.format(
                token,  random.uniform(0, 1), begin, fakeid)
            html_json = self.sess.get(url, headers=self.headers).json()
            # print(url)
            # print(html_json)
            app_msg_list = html_json['app_msg_list']
            if (str(app_msg_list) == '[]'):
                break
            for j in range(20):
                try:
                    if (app_msg_list[j]['title'] in Total_buf):
                        self.label_notes.setText("本条已存在，跳过")
                        print("本条已存在，跳过")
                        continue
                    title_buf.append(app_msg_list[j]['title'])
                    link_buf.append(app_msg_list[j]['link'])
                    img_buf.append(app_msg_list[j]['cover'])
                    Total_buf.append(app_msg_list[j]['title'])

                    table_count = self.tableWidget_result.rowCount()
                    if(table_index >= table_count):
                        self.tableWidget_result.insertRow(table_count)
                    # print("table_index：", table_index)
                    self.tableWidget_result.setItem(table_index, 0, QtWidgets.QTableWidgetItem(title_buf[j]))  # i*20+j
                    self.tableWidget_result.setItem(table_index, 1, QtWidgets.QTableWidgetItem(link_buf[j]))  # i*20+j
                    table_index = table_index + 1

                    with open(self.rootpath + "/spider.txt", 'a+') as fp:
                        fp.write('*' * 60 + '\nTitle: ' + title_buf[j] + '\nLink: ' + link_buf[j] + '\nImg: ' + img_buf[j] + '\r\n')
                        fp.close()
                        self.label_notes.setText(">> 第%d条写入完成：%s" % (j + 1, title_buf[j]))
                        print(">> 第%d条写入完成：%s" % (j + 1, title_buf[j]))
                except Exception as e:
                    print(">> 本页抓取结束 - ", e)
                    break
            self.label_notes.setText(">> 一页抓取结束，开始下载")
            print(">> 一页抓取结束，开始下载")
            self.get_content(title_buf, link_buf)
            title_buf.clear()  # 清除缓存
            link_buf.clear()  # 清除缓存
            self.label_notes.setText(">> 休息 %d s" % self.time_gap)
            print(">> 休息 %d s" % self.time_gap)
            sleep(self.time_gap)
        self.label_notes.setText(">> 抓取结束")

    def get_content(self, title_buf, link_buf):  # 获取地址对应的文章内容
        each_title = ""  # 初始化
        each_url = ""  # 初始化
        length = len(title_buf)

        for index in range(length):
            each_title = re.sub(r'[\|\/\<\>\:\*\?\\\"]', "_", title_buf[index])  # 剔除不合法字符
            filepath = self.rootpath + "/" + each_title  # 为每篇文章创建文件夹
            if (not os.path.exists(filepath)):  # 若不存在，则创建文件夹
                os.makedirs(filepath)
            os.chdir(filepath)  # 切换至文件夹

            html = self.sess.get(link_buf[index], headers=self.headers)
            soup = BeautifulSoup(html.text, 'lxml')
            article = soup.find(class_="rich_media_content").find_all("p")  # 查找文章内容位置
            img_urls = soup.find(class_="rich_media_content").find_all("img")  # 获得文章图片URL集

            # print("*" * 60)
            self.label_notes.setText(each_title)
            for i in article:
                line_content = i.get_text()  # 获取标签内的文本
                # print(line_content)
                if (line_content != None):  # 文本不为空
                    with open(each_title + r'.txt', 'a+', encoding='utf-8') as fp:
                        fp.write(line_content + "\n")  # 写入本地文件
                        fp.close()
            self.label_notes.setText(">> 保存文档 - 完毕!")
            print(">> 标题：", each_title)
            print(">> 保存文档 - 完毕!")
            for i in range(len(img_urls)):
                pic_down = requests.get(img_urls[i]["data-src"])
                with open(str(i) + r'.jpeg', 'ab+') as fp:
                    fp.write(pic_down.content)
                    fp.close()
            self.label_notes.setText(">> 保存图片%d张 - 完毕!\r\n" % len(img_urls))
            print(">> 保存图片%d张 - 完毕!\r\n" % len(img_urls))

################################强制关闭线程##################################################
    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)
###############################################################################################

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

