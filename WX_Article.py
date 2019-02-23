# -*- coding: utf-8 -*-

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

sess = requests.Session()
headers = {
    'Host': 'mp.weixin.qq.com',
    'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
}
global rootpath  # 全局变量，存放路径
global time_gap  # 全局变量，每页爬取等待时间

def Login(username, pwd):
    browser = webdriver.Firefox()
    # browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(r'https://mp.weixin.qq.com')
    browser.implicitly_wait(60)
    account = browser.find_element_by_name("account")
    password = browser.find_element_by_name("password")
    if(username!="" and pwd!=""):
        account.click()
        account.send_keys(username)
        password.click()
        password.send_keys(pwd)
        browser.find_element_by_xpath(r'//*[@id="header"]/div[2]/div/div/form/div[4]/a').click()
    else:
        print("* 请在10分钟内手动完成登录 *")
    WebDriverWait(browser, 60*10, 0.5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, r'.weui-desktop-account__nickname'))
    )
    print("登陆成功")
    token = re.search(r'token=(.*)', browser.current_url).group(1)
    cookies = browser.get_cookies()
    with open("cookie.json", 'w+') as fp:
        fp.write(json.dumps(cookies))
        print(">> 本地保存cookie")
        fp.write(json.dumps([{"token": token}]))
        print(">> 本地保存token")
        fp.close()
    browser.close()
    print('token:', token)
    return token, cookies


def Add_Cookies(cookie):
    c = requests.cookies.RequestsCookieJar()
    for i in cookie:  # 添加cookie到CookieJar
        c.set(i["name"], i["value"])
        sess.cookies.update(c)  # 更新session里的cookie


def Get_WeChat_Subscription(token, query):
    if(query==""):
        query = "xinhuashefabu1"
    url = r'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={0}&lang=zh_CN&f=json&ajax=1&random=0.5182749224035845&query={1}&begin=0&count=5'.format(token, query)
    html_json = sess.get(url, headers=headers).json()
    # print(html_json)
    fakeid = html_json['list'][0]['fakeid']
    nickname = html_json['list'][0]['nickname']
    print("fakeid:", fakeid)
    print("nickname: ", nickname)
    return fakeid, nickname

def Get_Articles(fakeid):
    title_buf = []
    link_buf = []
    img_buf = []

    Total_buf = []
    url = r'https://mp.weixin.qq.com/cgi-bin/appmsg?token={0}&lang=zh_CN&f=json&ajax=1&random=0.977467295649225&action=list_ex&begin=0&count=5&query=&fakeid={1}&type=9'.format(token, fakeid)
    html_json = sess.get(url, headers=headers).json()
    try:
        Total_Page = ceil(int(html_json['app_msg_cnt'])/5)
    except Exception as e:
        print("!! 失败信息：", html_json['base_resp']['err_msg'])
        return
    for i in range(Total_Page):
        print("第[%d/%d]页" % (i+1, Total_Page))
        begin = i * 5
        url = r'https://mp.weixin.qq.com/cgi-bin/appmsg?token={0}&lang=zh_CN&f=json&ajax=1&random=0.977467295649225&action=list_ex&begin={1}&count=5&query=&fakeid={2}&type=9'.format(token, begin, fakeid)
        html_json = sess.get(url, headers=headers).json()
        # print(html_json)
        app_msg_list = html_json['app_msg_list']
        if(str(app_msg_list) == '[]'):
            break
        for j in range(20):
            try:
                if(app_msg_list[j]['title'] in Total_buf):
                    print("本条已存在，跳过")
                    continue
                title_buf.append(app_msg_list[j]['title'])
                Total_buf.append(app_msg_list[j]['title'])
                link_buf.append(app_msg_list[j]['link'])
                img_buf.append(app_msg_list[j]['cover'])
                with open(rootpath+"/spider.txt", 'a+') as fp:
                    fp.write('*'*60+'\nTitle: '+title_buf[j]+'\nLink: '+link_buf[j]+'\nImg: '+img_buf[j]+'\r\n')
                    fp.close()
                    print(">> 第%d条写入完成：%s" % (j+1, title_buf[j]))
            except Exception as e:
                # print(">> 本页抓取结束")
                # print(e)
                break
        print(">> 一页抓取结束，开始下载")
        get_content(title_buf, link_buf)
        title_buf.clear()  # 清除缓存
        print(">> 休息 %d s" % time_gap)
        sleep(time_gap)
    print(">> 抓取结束")

def get_content(title_buf, link_buf):  # 获取地址对应的文章内容
    each_title = ""  # 初始化
    each_url = ""  # 初始化
    length = len(title_buf)

    for index in range(length):
        each_title = re.sub(r'[\|\/\<\>\:\*\?\\\"]', "_", title_buf[index])  # 剔除不合法字符
        filepath = rootpath + "/" + each_title  # 为每篇文章创建文件夹
        if(not os.path.exists(filepath)):  # 若不存在，则创建文件夹
            os.makedirs(filepath)
        os.chdir(filepath)  # 切换至文件夹

        html = sess.get(link_buf[index], headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')
        article = soup.find(class_="rich_media_content").find_all("p")  # 查找文章内容位置
        img_urls = soup.find(class_="rich_media_content").find_all("img")  # 获得文章图片URL集

        print("*" * 60)
        print(each_title)
        print(">> 保存文档 - ", end="")
        for i in article:
            line_content = i.get_text()  # 获取标签内的文本
            # print(line_content)
            if(line_content != None):  # 文本不为空
                with open(each_title+r'.txt', 'a+', encoding='utf-8') as fp:
                    fp.write(line_content + "\n")  # 写入本地文件
                    fp.close()
        print("完毕!")
        print(">> 保存图片 - %d张" % len(img_urls), end="")
        for i in range(len(img_urls)):
            pic_down = requests.get(img_urls[i]["data-src"])
            with open(str(i)+r'.jpeg', 'ab+') as fp:
                fp.write(pic_down.content)
                fp.close()
        print("完毕!\r\n")



if __name__ == '__main__':
    print("*"*100)
    print("* 程序原理:")
    print(">> 通过selenium登录获取token和cookie，再自动爬取和下载")
    print("* 使用前提： *")
    print(">> 电脑已装Firefox、Chrome、Opera、Edge等浏览器")
    print(">> 下载selenium驱动放入python安装目录，将目录添加至环境变量(https://www.seleniumhq.org/download/)")
    print(">> 申请一个微信公众号(https://mp.weixin.qq.com)")
    print("*" * 100)
    print("\r")

    query_name = input("输入公众号的英文名称，为空则默认新华社(xinhuashefabu1)：\n>> ")
    print("* 下面将输入自己公众号的账号密码(获取token和cookie)，为空则自动打开页面后手动输入 *")
    username = input("账号：")
    pwd = input("密码：")
    time_gap = input("输入每页爬取等待时间(一页约10条，越短越快被限制)，为空则默认为10s：\n>> ")
    if(time_gap == ""):
        time_gap = 10
    else:
        time_gap = int(time_gap)
    [token, cookies] = Login(username, pwd)
    # token = "1545909197"
    # cookies = json.loads(r'[{"name": "ua_id", "value": "azAJak7iTlXzTXbYAAAAAMF2DE9BeJukSX2cE1h4q_I=", "path": "/", "domain": "mp.weixin.qq.com", "secure": true, "httpOnly": true, "expiry": 2147483647}, {"name": "pgv_pvi", "value": "6558785536", "path": "/", "domain": ".qq.com", "secure": false, "httpOnly": false, "expiry": 2147385600}, {"name": "pgv_si", "value": "s2660289536", "path": "/", "domain": ".qq.com", "secure": false, "httpOnly": false}, {"name": "uuid", "value": "1d0109f7121d55bdf361bbe62056baa8", "path": "/", "domain": "mp.weixin.qq.com", "secure": true, "httpOnly": true}, {"name": "ticket", "value": "a3a0a44de8aba5a9c315518a3c863eabebff9780", "path": "/", "domain": "mp.weixin.qq.com", "secure": true, "httpOnly": true}, {"name": "ticket_id", "value": "gh_0c7b5742db32", "path": "/", "domain": "mp.weixin.qq.com", "secure": true, "httpOnly": true}, {"name": "cert", "value": "zr1b9NeHz9ugNlgGW9RyDTxcfBPSRX0J", "path": "/", "domain": "mp.weixin.qq.com", "secure": true, "httpOnly": true}, {"name": "noticeLoginFlag", "value": "1", "path": "/", "domain": "mp.weixin.qq.com", "secure": false, "httpOnly": false, "expiry": 1553303517}, {"name": "data_bizuin", "value": "3208951277", "path": "/", "domain": "mp.weixin.qq.com", "secure": true, "httpOnly": true}, {"name": "bizuin", "value": "3590155077", "path": "/", "domain": "mp.weixin.qq.com", "secure": true, "httpOnly": true}, {"name": "data_ticket", "value": "ENbWOnrXp2TIvyk2UhH57rT5LcZeOw583eTDkAmFIdJ6J5Kgx32LFvG7FYC9WjoD", "path": "/", "domain": "mp.weixin.qq.com", "secure": true, "httpOnly": true}, {"name": "slave_sid", "value": "ZmFhaFNPZzFOeHhPTDI0dzlaSzlMWXdITEJUc25LSmFXSEVHNllPRmFOZ3NJWmNfczA3MjZWcjlMbk1KX2NGb2tBWTRiOXJfWXlmMDI5YjZqM3ZUT3BTVnN6b2drdHVqU1VGUUJuRWM4dXlVS2hwWTdHUkxReDFST2Z3Q0dCaGFhbmVTaW91Z0pxNkZHNEVt", "path": "/", "domain": "mp.weixin.qq.com", "secure": true, "httpOnly": true}, {"name": "slave_user", "value": "gh_0c7b5742db32", "path": "/", "domain": "mp.weixin.qq.com", "secure": true, "httpOnly": true}, {"name": "xid", "value": "d277e59a8b956fa77a53e963b3e8ef8f", "path": "/", "domain": "mp.weixin.qq.com", "secure": true, "httpOnly": true, "expiry": 2147483647}, {"name": "openid2ticket_o7bVEvy2EtsmKCeePaZBz9QlN-8E", "value": "YI7ZDtE9JzAT3WBQDLmA52ESIwAqS3qPWdQDatSc8t0=", "path": "/", "domain": "mp.weixin.qq.com", "secure": true, "httpOnly": true, "expiry": 1553303536}, {"name": "mm_lang", "value": "zh_CN", "path": "/", "domain": "mp.weixin.qq.com", "secure": true, "httpOnly": false, "expiry": 4294967295}]')
    Add_Cookies(cookies)
    [fakeid, nickname] = Get_WeChat_Subscription(token, query_name)
    rootpath = os.getcwd() + r"/spider/" + nickname
    Get_Articles(fakeid)

