# -*- coding: utf-8 -*-
import WeChat
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import re
from time import sleep, localtime, time, strftime

from PyQt5.QtWidgets import QApplication
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
from goto import with_goto
import configparser

'''
conf.ini
    [resume]
    rootpath = ''
    pagenum = 0
    linkbuf_cnt = 0
    download_cnt = 0
'''
# 设置 递归调用深度 为 一百万
sys.setrecursionlimit(1000000)

# title_buf = []
# link_buf = []
pro_continue = 0
class MyMainWindow(WeChat.Ui_MainWindow):
    def __init__(self):
        self.sess = requests.Session()
        self.headers = {
            'Host': 'mp.weixin.qq.com',
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
        }
        self.initpath = os.getcwd()
        self.rootpath = os.getcwd() + r"/spider/"  # 全局变量，存放路径
        self.time_gap = 5       # 全局变量，每页爬取等待时间
        self.timeStart = 1999   # 全局变量，起始时间

        self.year_now = localtime(time()).tm_year  # 当前年份，用于比对时间
        self.timeEnd = self.year_now+1     # 全局变量，结束时间
        self.thread_list = []
        self.label_debug_string = ""
        self.label_debug_cnt = 0
        self.total_articles = 0  # 当前文章数
        self.keyWord = ""
        self.keyword_search_mode = 0
        self.keyWord_2 = ""
        self.freq_control = 0
        self.download_cnt = 0
        self.linkbuf_cnt = 0
        self.download_end = 0
        self.isresume = self.Check_Config()
        self.url_json_init()
        self.title_buf = []
        self.link_buf = []

    def vari_init(self):
        # global title_buf, link_buf
        self.rootpath = os.getcwd() + r"/spider/"  # 全局变量，存放路径
        self.thread_list = []
        self.label_debug_string = ""
        self.label_debug_cnt = 0
        self.total_articles = 0  # 当前文章数
        self.keyWord = ""
        self.keyword_search_mode = 0
        self.keyWord_2 = ""
        self.Label_Debug(' ')
        self.freq_control = 0
        self.download_cnt = 0
        self.linkbuf_cnt = 0
        self.download_end = 0
        self.title_buf.clear()  # 清除缓存
        self.link_buf.clear()  # 清除缓存
        # self.progressBar.setMaximum(100)
        # self.progressBar.setValue(0)

    def Label_Debug(self, string):
        if self.label_debug_cnt == 12:
            self.label_debug_string = ""
            self.label_notes.setText(self.label_debug_string)
            self.label_debug_cnt = 0
        self.label_debug_string += "\r\n" + string
        self.label_notes.setText(self.label_debug_string)
        self.label_debug_cnt += 1

    def Label_Debug_Clear(self):
        self.label_debug_string = ""
        self.label_notes.setText(self.label_debug_string)
        self.label_notes.clear()
        self.label_debug_cnt = 0

    def setupUi(self, MainWindow):
        super(MyMainWindow, self).setupUi(MainWindow)
        try:
            with open(os.getcwd()+r'/login.json', 'r', encoding='utf-8') as p:
                login_dict = json.load(p)
                print("登陆文件读取成功")
                self.Label_Debug("登陆文件读取成功")
                self.LineEdit_target.setText(login_dict['target'])  # 公众号的英文名称
                self.LineEdit_user.setText(login_dict['user'])  # 自己公众号的账号
                self.LineEdit_pwd.setText(login_dict['pwd'])  # 自己公众号的密码
                self.LineEdit_timegap.setText(str(login_dict['timegap']))  # 每页爬取等待时间"
                self.lineEdit_timeEnd.setText(str(self.year_now+1))  # 结束时间为当前年
                self.lineEdit_timeStart.setText("1999")  # 开始时间为1999
                QApplication.processEvents()  # 刷新文本操作
                p.close()
        except Exception as e:
            print(e)

    def Start_Run(self):
        self.total_articles = 0
        Process_thread = threading.Thread(target=self.Process, daemon=True)
        Process_thread.start()
        self.thread_list.append(Process_thread)

    def Stop_Run(self):
        try:
            self.stop_thread(self.thread_list.pop())
            self.stop_thread(self.thread_list.pop())
            self.vari_init()  # 变量复位
            self.Label_Debug("终止成功!")
            print("终止成功!")
        except Exception as e:
            print(e)

    def Start_Run_2(self):
        try:
            os.makedirs(self.rootpath)
        except:
            pass
        self.keyword_search_mode = 1
        self.total_articles = 0
        Process_thread = threading.Thread(target=self.Process, daemon=True)
        Process_thread.start()
        self.thread_list.append(Process_thread)

    def Stop_Run_2(self):
        try:
            self.keyword_search_mode = 0
            self.stop_thread(self.thread_list.pop())
            self.stop_thread(self.thread_list.pop())
            self.vari_init()  # 变量复位
            self.Label_Debug("终止成功!")
            print("终止成功!")
        except Exception as e:
            print(e)

    def Change_IP(self):
        tar_url = r'https://www.douban.com'
        http_s = '111.26.9.26:80'
        if (tar_url.split(':')[0] == 'https'):
            proxies = {'https': http_s}
        else:
            proxies = {'http': http_s}
        try:
            # sess = requests.session()
            html = self.sess.get(tar_url, proxies=proxies, timeout=(30, 60))
            print("* 代理有效√ *")
            print(html)
        except Exception as e:
            print("* 代理无效× *")
            print(e)
        pass

    def Check_Config(self):
        self.conf = configparser.ConfigParser()
        self.cfgpath = os.path.join(os.getcwd(), "conf.ini")
        if os.path.exists(self.cfgpath):
            print("[Yes] conf.ini")
            try:
                self.conf.read(self.cfgpath, encoding="utf8")  # 读ini文件
            except:
                self.conf.read(self.cfgpath)  # 读ini文件
            resume = self.conf.items('resume')
            self.rootpath       = resume[0][1]
            self.pagenum        = int(resume[1][1])
            self.linkbuf_cnt    = int(resume[2][1])
            self.download_cnt   = int(resume[3][1])
            self.total_articles = int(resume[4][1])
            print(self.rootpath, self.pagenum, self.linkbuf_cnt, self.download_cnt, self.total_articles)
            return 1
        else:
            print("[NO] conf.ini")
            f = open(self.cfgpath, 'w', encoding="utf-8")
            f.close()
            self.conf.add_section("resume")
            self.conf.set("resume", "rootpath", os.getcwd())
            self.conf.set("resume", "pagenum", "0")
            self.conf.set("resume", "linkbuf_cnt", "0")
            self.conf.set("resume", "download_cnt", "0")
            self.conf.set("resume", "total_articles", "0")
            self.conf.write(open(self.cfgpath, "w"))  # 删除原文件重新写入
            return 0

    def Process(self):
        try:
            username = self.LineEdit_user.text()  # 自己公众号的账号
            pwd = self.LineEdit_pwd.text()  # 自己公众号的密码
            query_name = self.LineEdit_target.text()                 # 公众号的英文名称
            self.time_gap = self.LineEdit_timegap.text() or 10       # 每页爬取等待时间
            self.time_gap = int(self.time_gap)
            self.timeStart = self.lineEdit_timeStart.text() or 1999  # 起始时间
            self.timeStart = int(self.timeStart)
            self.timeEnd = self.lineEdit_timeEnd.text() or self.year_now+1      # 结束时间
            self.timeEnd = int(self.timeEnd)
            self.keyWord = self.lineEdit_keyword.text()              # 关键词

            if self.checkBox.isChecked() is True and pwd != "":
                dict = {'target': query_name, 'user': username, 'pwd': pwd, 'timegap': self.time_gap}
                with open(os.getcwd()+r'/login.json', 'w+') as p:
                    json.dump(dict, p)
                    p.close()

            [token, cookies] = self.Login(username, pwd)
            self.Add_Cookies(cookies)
            if self.keyword_search_mode == 1:
                self.keyWord_2 = self.lineEdit_keyword_2.text()  # 关键词
                self.KeyWord_Search(token, self.keyWord_2)
            else:
                [fakeid, nickname] = self.Get_WeChat_Subscription(token, query_name)
                if self.isresume == 0:
                    Index_Cnt = 0
                    while True:
                        try:
                            self.rootpath = os.path.join(os.getcwd(), "spider-%d" % Index_Cnt, nickname) #+ r"/spider-%d/" % Index_Cnt + nickname  # !!!!!!!!!!!!!!
                            os.makedirs(self.rootpath)
                            self.conf.set("resume", "rootpath", self.rootpath)
                            self.conf.write(open(self.cfgpath, "r+", encoding="utf-8"))
                            break
                        except:
                            Index_Cnt = Index_Cnt + 1
                self.Get_Articles(token, fakeid)
        except Exception as e:
            self.Label_Debug("!!![%s]" % str(e))
            print("!!![%s]" % str(e))
            if "list" in str(e):
                self.Label_Debug("请删除cookie.json")
                print("请删除cookie.json")

    def url_json_write(self, inputdict):
        with open(self.url_json_path, "w+") as f:
            f.write(json.dumps(inputdict))

    def url_json_read(self):
        with open(self.url_json_path, "r+") as f:
            json_read = json.loads(f.read())
        return json_read

    def url_json_update(self, source, adddict):
        source.append(adddict)

    def url_json_init(self):
        self.url_json_path = os.path.join(os.getcwd(), "url.json")
        if os.path.exists(self.url_json_path):
            print("[Yes] url.json")
            if self.isresume == 0:
                os.remove(self.url_json_path)
                self.url_json_write([])
        else:
            print("[NO] url.json")
            self.url_json_write([])
        self.json_read = self.url_json_read()
        self.json_read_len = len(self.json_read)
        print("len(url.json):", self.json_read_len)

    def url_json_once(self, dict_add):
        self.url_json_update(self.json_read, dict_add)  # {"Title": 1, "Link": 2, "Img": 3}
        self.url_json_write(self.json_read)
        self.json_read = self.url_json_read()
        # print("url_json_once OK")
        # print(self.json_read)

    def Login(self, username, pwd):
        try:
            if self.freq_control == 1:
                raise RuntimeError('freq_control=1')
            print(self.initpath+"/cookie.json")
            with open(self.initpath+"/cookie.json", 'r+') as fp:
                cookieToken_dict = json.load(fp)
                cookies = cookieToken_dict[0]['COOKIES']
                token = cookieToken_dict[0]['TOKEN']
                print(token)
                print(cookies)

                if cookies != "" and token != "":
                    self.Label_Debug("cookie.json读取成功")
                    print("cookie.json读取成功")
                self.Add_Cookies(cookies)

                html = self.sess.get(r'https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=%s' % token, timeout=(30, 60))
                if "登陆" not in html.text:
                    self.Label_Debug("cookie有效,无需浏览器登陆")
                    print("cookie有效,无需浏览器登陆")
                    return token, cookies
        except Exception as e:
            print("无cookie.json或失效 -", e)
            self.Label_Debug("无cookie.json或失效")


        self.Label_Debug("正在打开浏览器,请稍等")
        print("正在打开浏览器,请稍等")
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
            self.Label_Debug("* 请在10分钟内手动完成登录 *")
        WebDriverWait(browser, 60 * 10, 0.5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, r'.weui-desktop-account__nickname'))
        )
        self.Label_Debug("登陆成功")
        token = re.search(r'token=(.*)', browser.current_url).group(1)
        cookies = browser.get_cookies()
        with open(os.getcwd()+"/cookie.json", 'w+') as fp:
            temp_list = {}
            temp_array = []
            temp_list['COOKIES'] = cookies
            temp_list['TOKEN'] = token
            temp_array.append(temp_list)
            json.dump(temp_array, fp)
            fp.close()
            self.Label_Debug(">> 本地保存cookie和token")
            print(">> 本地保存cookie和token")
        browser.close()
        return token, cookies

    def Add_Cookies(self, cookie):
        c = requests.cookies.RequestsCookieJar()
        for i in cookie:  # 添加cookie到CookieJar
            c.set(i["name"], i["value"])
            self.sess.cookies.update(c)  # 更新session里的cookie

    def KeyWord_Search(self, token, keyword):
        self.url_buf = []
        self.title_buf = []
        header = {
            'Content - Type': r'application/x-www-form-urlencoded;charset=UTF-8',
            'Host': 'mp.weixin.qq.com',
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&share=1&lang=zh_CN&token=%d' % int(token)
        }
        url = r'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?sub=check_appmsg_copyright_stat'
        data = {'token': token, 'lang': 'zh_CN', 'f': 'json', 'ajax': 1, 'random': random.uniform(0, 1), 'url': keyword, 'allow_reprint': 0, 'begin': 0, 'count': 10}
        html_json = self.sess.post(url, data=data, headers=header).json()
        total = html_json['total']
        total_page = ceil(total / 10)
        print(total_page, '-', total)
        table_index = 0
        for i in range(total_page):
            data = {
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': 1,
                'random': random.uniform(0, 1),
                'url': keyword,
                'allow_reprint': 0,
                'begin': i*10,
                'count': 10
            }
            html_json = self.sess.post(url, data=data, headers=header).json()
            page_len = len(html_json['list'])
            # print(page_len)
            for j in range(page_len):
                self.url_buf.append(html_json['list'][j]['url'])
                self.title_buf.append(html_json['list'][j]['title'])
                print(j+1, ' - ', html_json['list'][j]['title'])
                table_count = self.tableWidget_result.rowCount()
                if (table_index >= table_count):
                    self.tableWidget_result.insertRow(table_count)
                self.tableWidget_result.setItem(table_index, 0, QtWidgets.QTableWidgetItem(self.title_buf[j]))  # i*20+j
                self.tableWidget_result.setItem(table_index, 1, QtWidgets.QTableWidgetItem(self.url_buf[j]))  # i*20+j
                table_index = table_index + 1
                self.total_articles += 1
                with open(self.rootpath + "/spider.txt", 'a+', encoding="utf-8") as fp:
                    fp.write('*' * 60 + '\n【%d】\n  Title: ' % self.total_articles + self.title_buf[j] + '\n  Link: ' + self.url_buf[j] + '\n  Img: ' + '\r\n\r\n')
                    # fp.write('\n【%d】\n' % self.total_articles + '\n' + url_buf[j] + '\r\n')
                    fp.close()
                    self.Label_Debug(">> 第%d条写入完成：%s" % (j + 1, self.title_buf[j]))
                    print(">> 第%d条写入完成：%s" % (j + 1, self.title_buf[j]))
            print('*' * 60)
            self.get_content(self.title_buf, self.url_buf)
            self.url_buf.clear()
            self.title_buf.clear()

    def Get_WeChat_Subscription(self, token, query):
        if (query == ""):
            query = "xinhuashefabu1"
        url = r'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={0}&lang=zh_CN&f=json&ajax=1&random=0.5182749224035845&query={1}&begin=0&count=5'.format(
            token, query)
        html_json = self.sess.get(url, headers=self.headers, timeout=(30, 60)).json()
        fakeid = html_json['list'][0]['fakeid']
        nickname = html_json['list'][0]['nickname']
        self.Label_Debug("nickname: "+nickname)
        return fakeid, nickname

    def Get_Articles(self, token, fakeid):
        # title_buf = []
        # link_buf = []
        img_buf = []

        Total_buf = []
        url = r'https://mp.weixin.qq.com/cgi-bin/appmsg?token={0}&lang=zh_CN&f=json&ajax=1&random={1}&action=list_ex&begin=0&count=5&query=&fakeid={2}&type=9'.format(token,  random.uniform(0, 1), fakeid)
        html_json = self.sess.get(url, headers=self.headers, timeout=(30, 60)).json()
        try:
            Total_Page = ceil(int(html_json['app_msg_cnt']) / 5)
            # self.progressBar.setMaximum(Total_Page)
            QApplication.processEvents()  # 刷新文本操作
        except Exception as e:
            print(e)
            self.Label_Debug("!! 失败信息："+html_json['base_resp']['err_msg'])
            if 'freq control' in html_json['base_resp']['err_msg']:
                if self.LineEdit_user_2.text() != '' and self.LineEdit_pwd_2.text() != '':
                    self.freq_control = 1
                    self.Label_Debug("将使用备胎公众号")
                    username = self.LineEdit_user_2.text()  # 备选公众号的账号
                    pwd = self.LineEdit_pwd_2.text()  # 备选公众号的密码
                    [token, cookies] = self.Login(username, pwd)
                    self.Add_Cookies(cookies)
                    self.freq_control = 0
                    self.Get_Articles(token, fakeid)
            return
        table_index = 0

        download_thread = threading.Thread(target=self.download_content)
        download_thread.start()
        self.thread_list.append(download_thread)

        _buf_index = 0
        for i in range(Total_Page):
            if self.isresume == 1:
                i = i + self.pagenum
            self.Label_Debug("第[%d/%d]页  url:%s, article:%s" % (i + 1, Total_Page, self.linkbuf_cnt, self.download_cnt))
            print("第[%d/%d]页  url:%s, article:%s" % (i + 1, Total_Page, self.linkbuf_cnt, self.download_cnt))
            self.label_total_Page.setText("第[%d/%d]页  linkbuf_cnt:%s, download_cnt:%s" % (i + 1, Total_Page, self.linkbuf_cnt, self.download_cnt))
            begin = i * 5
            url = r'https://mp.weixin.qq.com/cgi-bin/appmsg?token={0}&lang=zh_CN&f=json&ajax=1&random={1}&action=list_ex&begin={2}&count=5&query=&fakeid={3}&type=9'.format(
                token,  random.uniform(0, 1), begin, fakeid)
            while True:
                try:
                    html_json = self.sess.get(url, headers=self.headers, timeout=(30, 60)).json()
                    break
                except Exception as e:
                    print("连接出错，稍等2s", e)
                    self.Label_Debug("连接出错，稍等2s" + str(e))
                    sleep(2)
                    continue
            try:
                app_msg_list = html_json['app_msg_list']
            except Exception as e:
                self.Label_Debug("！！！操作太频繁，5s后重试！！！")
                print("！！！操作太频繁，5s后重试！！！", e)
                sleep(5)
                continue
                # os._exit(0)

            if (str(app_msg_list) == '[]'):
                print('结束了')
                self.Label_Debug("结束了")
                break
            for j in range(30):
                try:
                    if (app_msg_list[j]['title'] in Total_buf):
                        self.Label_Debug("本条已存在，跳过")
                        print("本条已存在，跳过")
                        continue
                    if self.keyWord != "":
                        if self.keyWord not in app_msg_list[j]['title']:
                            self.Label_Debug("本条不匹配关键词[%s]，跳过" % self.keyWord)
                            print("本条不匹配关键词[%s]，跳过" % self.keyWord)
                            continue
                    article_time = int(strftime("%Y", localtime(int(app_msg_list[j]['update_time']))))  # 当前文章时间戳转为年份
                    if (self.timeStart > article_time):
                        self.Label_Debug("本条[%d]不在时间范围[%d-%d]内，跳过" % (article_time, self.timeStart, self.timeEnd))
                        print("本条[%d]不在时间范围[%d-%d]内，跳过" % (article_time, self.timeStart, self.timeEnd))
                        continue
                    if(article_time > self.timeEnd):
                        self.Label_Debug("达到结束时间，退出")
                        print("达到结束时间，退出")
                        self.Stop_Run()
                        return
                        # os._exit(0)
                    self.title_buf.append(app_msg_list[j]['title'])
                    self.link_buf.append(app_msg_list[j]['link'])
                    img_buf.append(app_msg_list[j]['cover'])
                    Total_buf.append(app_msg_list[j]['title'])

                    table_count = self.tableWidget_result.rowCount()
                    if(table_index >= table_count):
                        self.tableWidget_result.insertRow(table_count)
                    self.tableWidget_result.setItem(table_index, 0, QtWidgets.QTableWidgetItem(self.title_buf[_buf_index+j]))  # i*20+j
                    self.tableWidget_result.setItem(table_index, 1, QtWidgets.QTableWidgetItem(self.link_buf[_buf_index+j]))  # i*20+j
                    table_index = table_index + 1

                    self.total_articles += 1
                    dict_in = {"Title": self.title_buf[_buf_index+j], "Link": self.link_buf[_buf_index+j], "Img": img_buf[_buf_index+j]}
                    self.url_json_once(dict_in)
                    with open(self.rootpath + "/spider.txt", 'a+', encoding="utf-8") as fp:
                        fp.write('*' * 60 + '\n【%d】\n  Title: ' % self.total_articles + self.title_buf[_buf_index+j] + '\n  Link: ' + self.link_buf[_buf_index+j] + '\n  Img: ' + img_buf[_buf_index+j] + '\r\n\r\n')
                        # fp.write('【%d】 ' % self.total_articles + '\n' + link_buf[j] + '\r\n')
                        fp.close()
                    self.Label_Debug(">> 第%d条写入完成：%s" % (self.total_articles, self.title_buf[_buf_index+j]))
                    print(">> 第%d条写入完成：%s" % (self.total_articles, self.title_buf[_buf_index+j]))
                    self.conf.set("resume", "total_articles", str(self.total_articles))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    self.conf.write(open(self.cfgpath, "r+", encoding="utf-8"))
                except Exception as e:
                    print(">> 本页抓取结束 - ", e)
                    _buf_index += j
                    print(_buf_index, len(self.title_buf))
                    print(self.title_buf)
                    break

            self.Label_Debug(">> 一页抓取结束")
            print(">> 一页抓取结束")
            # self.get_content(title_buf, link_buf)
            # title_buf.clear()  # 清除缓存
            # link_buf.clear()  # 清除缓存
            if self.isresume == 1:
                self.linkbuf_cnt = len(self.link_buf) + self.json_read_len
            else:
                self.linkbuf_cnt = len(self.link_buf)
            self.conf.set("resume", "linkbuf_cnt", str(self.linkbuf_cnt))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.conf.write(open(self.cfgpath, "r+", encoding="utf-8"))
            self.conf.set("resume", "pagenum", str(i))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.conf.write(open(self.cfgpath, "r+", encoding="utf-8"))
            sleep(self.time_gap)
        self.Label_Debug_Clear()
        self.Label_Debug(">> 列表抓取结束!!! <<")
        print(">> 列表抓取结束!!! <<")
        self.download_end = 1


    def download_content(self):
        # global link_buf, title_buf
        # self.pri_index = 0
        while 1:
            try:
                if self.download_cnt < self.linkbuf_cnt:
                    if self.isresume == 1:
                        self.json_read = self.url_json_read()
                        # print("download_cnt:", self.download_cnt, "; json_read:", len(self.json_read), "; linkbuf_cnt:", self.linkbuf_cnt)
                        self.get_content(self.json_read[self.download_cnt]["Title"], self.json_read[self.download_cnt]["Link"])
                    else:
                        self.get_content(self.title_buf[self.download_cnt], self.link_buf[self.download_cnt])
                    self.download_cnt += 1
                    self.conf.set("resume", "download_cnt", str(self.download_cnt))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    self.conf.write(open(self.cfgpath, "r+", encoding="utf-8"))
                elif self.download_cnt >= self.linkbuf_cnt and self.download_end == 1:
                    self.Label_Debug_Clear()
                    self.Label_Debug(">> 程序结束, 欢迎再用!!! <<")
                    print(">> 程序结束, 欢迎再用!!! <<")
                    break
                elif self.download_cnt == self.linkbuf_cnt and self.download_end == 0:
                    sleep(2)
            except Exception as e:
                print("download_content", e)
                self.Label_Debug(e)


    def get_content(self, title_buf, link_buf):  # 获取地址对应的文章内容
        each_title = ""  # 初始化
        each_url = ""  # 初始化
        if self.keyword_search_mode == 1:
            length = len(title_buf)
        else:
            length = 1

        for index in range(length):
            if self.keyword_search_mode == 1:
                each_title = re.sub(r'[\|\/\<\>\:\*\?\\\"]', "_", title_buf[index])  # 剔除不合法字符
            else:
                each_title = re.sub(r'[\|\/\<\>\:\*\?\\\"]', "_", title_buf)  # 剔除不合法字符
            filepath = self.rootpath + "/" + each_title  # 为每篇文章创建文件夹
            if (not os.path.exists(filepath)):  # 若不存在，则创建文件夹
                os.makedirs(filepath)
            os.chdir(filepath)  # 切换至文件夹

            while True:
                try:
                    if self.keyword_search_mode == 1:
                        html = self.sess.get(link_buf[index], headers=self.headers, timeout=(30, 60))
                    else:
                        html = self.sess.get(link_buf, headers=self.headers, timeout=(30, 60))
                    break
                except Exception as e:
                    print("连接出错，稍等2s", e)
                    self.Label_Debug("连接出错，稍等2s" + str(e))
                    sleep(2)
                    continue

            soup = BeautifulSoup(html.text, 'lxml')
            try:
                article = soup.find(class_="rich_media_content").find_all("p")  # 查找文章内容位置
                No_article = 0
            except Exception as e:
                No_article = 1
                self.Label_Debug("本篇未匹配到文字 ->"+str(e))
                print("本篇未匹配到文字 ->", e)
                pass
            try:
                img_urls = soup.find(class_="rich_media_content").find_all("img")  # 获得文章图片URL集
                No_img = 0
            except Exception as e:
                No_img = 1
                self.Label_Debug("本篇未匹配到图片 ->" + str(e))
                print("本篇未匹配到图片 ->", e)
                pass

            print("*" * 60)
            self.Label_Debug("*" * 30)
            self.Label_Debug(each_title)
            if No_article != 1:
                for i in article:
                    line_content = i.get_text()  # 获取标签内的文本
                    # print(line_content)
                    if (line_content != None):  # 文本不为空
                        with open(each_title + r'.txt', 'a+', encoding='utf-8') as fp:
                            fp.write(line_content + "\n")  # 写入本地文件
                            fp.close()
                self.Label_Debug(">> 保存文档 - 完毕!")
                # print(">> 标题：", each_title)
                print(">> 保存文档 - 完毕!")
            if No_img != 1:
                for i in range(len(img_urls)):
                    re_cnt = 0
                    while True:
                        try:
                            pic_down = self.sess.get(img_urls[i]["data-src"], timeout=(30, 60))  # 连接超时30s，读取超时60s，防止卡死
                            break
                        except Exception as e:
                            print("下载超时 ->", e)
                            self.Label_Debug("下载超时->" + str(e))
                            re_cnt += 1
                            if re_cnt > 3:
                                print("放弃此图")
                                self.Label_Debug("放弃此图")
                                break
                    if re_cnt > 3:
                        f = open(str(i) + r'.jpeg', 'ab+')
                        f.close()
                        continue
                    img_urls[i]["src"] = str(i)+r'.jpeg'  # 更改图片地址为本地
                    with open(str(i) + r'.jpeg', 'ab+') as fp:
                        fp.write(pic_down.content)
                        fp.close()
                self.Label_Debug(">> 保存图片%d张 - 完毕!" % len(img_urls))
                print(">> 保存图片%d张 - 完毕!" % len(img_urls))

            with open(each_title+r'.html', 'w', encoding='utf-8') as f:  # 保存html文件
                f.write(str(soup))
                f.close()
                self.Label_Debug(">> 保存html - 完毕!")
                print(">> 保存html - 完毕!")
            if self.keyword_search_mode == 1:
                self.Label_Debug(">> 休息 %d s" % self.time_gap)
                print(">> 休息 %d s" % self.time_gap)
                sleep(self.time_gap)

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

