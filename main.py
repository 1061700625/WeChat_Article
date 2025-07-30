# -*- coding: utf-8 -*-
# 设置文件编码为 UTF-8，支持中文字符处理

import json  # 用于处理 JSON 文件读写
import os  # 用于文件和目录操作
import random  # 用于生成随机数（如请求参数中的随机值）
import re  # 用于正则表达式匹配
import threading  # 用于多线程操作
import time  # 用于时间处理和延时
from math import ceil  # 用于计算分页数（向上取整）
from pathlib import Path  # 用于跨平台路径处理

import configparser  # 用于解析和写入配置文件（conf.ini）
import pyautogui  # 用于弹出提示框（如登录提醒）
import requests  # 用于发送 HTTP 请求
from bs4 import BeautifulSoup  # 用于解析 HTML 内容
from PyQt5 import QtCore, QtGui, QtWidgets  # PyQt5 核心模块，用于 GUI 界面
from PyQt5.QtCore import Qt  # PyQt5 核心常量（如对齐方式）
from PyQt5.QtGui import QPixmap  # 用于处理图片显示
from selenium import webdriver  # 用于自动化浏览器操作
from selenium.webdriver.chrome.options import Options  # 配置 Chrome 浏览器选项
from selenium.webdriver.chrome.service import Service  # 配置 ChromeDriver 服务
from selenium.webdriver.common.by import By  # 用于定位网页元素
from selenium.webdriver.support import expected_conditions as EC  # 用于等待条件判断
from selenium.webdriver.support.ui import WebDriverWait  # 用于显式等待
from webdriver_manager.chrome import ChromeDriverManager  # 自动管理 ChromeDriver

import sys  # 系统相关操作（如设置递归深度）
import ctypes  # 用于低级别线程控制（如强制终止线程）
import inspect  # 用于检查对象类型（如线程异常处理）
import WeChat  # 自定义模块，提供界面基础类 Ui_MainWindow

# 设置递归深度为100万，避免递归调用过深导致栈溢出
sys.setrecursionlimit(1_000_000)


class MyMainWindow(WeChat.Ui_MainWindow):
    """微信爬虫主窗口类，继承自 WeChat.Ui_MainWindow
    
    该类负责管理微信公众号文章爬取的图形界面和核心逻辑，包括登录、文章抓取、内容下载等功能。
    """

    def __init__(self):
        """初始化主窗口和全局变量
        
        初始化爬虫所需的变量，包括网络请求会话、文件路径、时间参数、线程列表等。
        """
        # 创建一个 HTTP 会话对象，用于持久化的网络请求
        self.session = requests.Session()
        # 设置默认的 HTTP 请求头，模拟浏览器访问
        self.headers = {
            "Host": "mp.weixin.qq.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
        }
        # 浏览器和驱动程序的路径（未使用，保留以兼容可能的未来需求）
        self.browser_path = "Chrome/BitBrowser.exe"
        self.driver_path = "Chrome/chromedriver.exe"

        # 初始化工作目录和默认存储路径
        self.init_path = os.getcwd()  # 获取当前工作目录
        self.root_path = os.path.join(self.init_path, "spider")  # 存储爬取结果的根目录
        self.time_gap = 5  # 每页爬取之间的默认等待时间（秒）
        self.time_start = 1999  # 默认起始年份
        self.year_now = time.localtime().tm_year  # 获取当前年份
        self.time_end = self.year_now + 1  # 默认结束年份为下一年

        # 初始化线程管理和调试信息
        self.thread_list = []  # 存储运行中的线程
        self.label_debug_string = ""  # 调试信息字符串，用于界面显示
        self.label_debug_count = 0  # 调试信息行计数，用于控制显示行数
        self.total_articles = 0  # 已爬取的文章总数
        self.keyword = ""  # 搜索关键词
        self.keyword_search_mode = 0  # 关键词搜索模式开关（0: 公众号模式, 1: 关键词模式）
        self.keyword_2 = ""  # 第二个关键词（用于关键词搜索模式）
        self.freq_control = 0  # 频率控制标志，用于处理访问限制
        self.download_count = 0  # 已下载的文章数
        self.link_buffer_count = 0  # 链接缓冲区计数
        self.download_end = 0  # 下载结束标志
        self.is_resume = self._check_config()  # 检查是否从断点恢复
        self._init_url_json()  # 初始化 URL 存储的 JSON 文件
        self.title_buffer = []  # 文章标题缓冲区
        self.link_buffer = []  # 文章链接缓冲区
        self.wechat_uin = None  # 微信 UIN（未使用，保留以兼容评论功能）
        self.wechat_key = None  # 微信 Key（未使用，保留以兼容评论功能）

    def _init_variables(self):
        """初始化或重置变量
        
        在启动新任务或停止任务时，重置所有全局变量到初始状态。
        """
        self.root_path = os.path.join(os.getcwd(), "spider")  # 重置存储路径
        self.thread_list = []  # 清空线程列表
        self.label_debug_string = ""  # 清空调试信息
        self.label_debug_count = 0  # 重置调试计数
        self.total_articles = 0  # 重置文章总数
        self.keyword = ""  # 清空关键词
        self.keyword_search_mode = 0  # 重置搜索模式
        self.keyword_2 = ""  # 清空第二个关键词
        self._label_debug(" ")  # 在界面显示空行
        self.freq_control = 0  # 重置频率控制
        self.download_count = 0  # 重置下载计数
        self.link_buffer_count = 0  # 重置链接缓冲计数
        self.download_end = 0  # 重置下载结束标志
        self.title_buffer.clear()  # 清空标题缓冲区
        self.link_buffer.clear()  # 清空链接缓冲区
        self.progressBar.setMaximum(100)  # 设置进度条最大值
        self.progressBar.setValue(0)  # 重置进度条值为0

    def _label_debug(self, message):
        """更新调试信息标签
        
        在界面上的调试标签中追加消息，控制显示行数不超过12行。
        
        Args:
            message (str): 要显示的调试信息
        """
        if self.label_debug_count >= 12:  # 如果超过12行，清空并重置
            self.label_debug_string = ""
            self.label_notes.setText(self.label_debug_string)
            self.label_debug_count = 0
        self.label_debug_string += f"\n{message}"  # 追加新消息
        self.label_notes.setText(self.label_debug_string)  # 更新界面显示
        self.label_debug_count += 1  # 增加行计数

    def _clear_label_debug(self):
        """清除调试信息
        
        清空调试标签的内容并重置计数。
        """
        self.label_debug_string = ""
        self.label_notes.clear()  # 清空界面上的调试信息
        self.label_debug_count = 0

    def setupUi(self, MainWindow):
        """设置用户界面
        
        初始化图形界面，包括加载配置文件中的默认值和显示二维码图片。
        注意：此方法名与父类一致，直接覆盖父类的实现。
        
        Args:
            MainWindow (QtWidgets.QMainWindow): 主窗口对象
        """
        super().setupUi(MainWindow)  # 调用父类的界面设置方法，保持信号连接
        try:
            login_file = os.path.join(self.init_path, "login.json")  # 登录信息文件路径
            if os.path.exists(login_file):  # 如果存在登录配置文件
                with open(login_file, "r", encoding="utf-8") as file:
                    login_data = json.load(file)  # 读取 JSON 数据
                    self._label_debug("登录文件读取成功")
                    # 设置界面上的文本框内容
                    self.LineEdit_target.setText(login_data["target"])  # 目标公众号
                    self.LineEdit_user.setText(login_data["user"])  # 用户名
                    self.LineEdit_pwd.setText(login_data["pwd"])  # 密码
                    self.LineEdit_timegap.setText(str(login_data["timegap"]))  # 爬取间隔
                    self.lineEdit_timeEnd.setText(str(self.year_now + 1))  # 结束年份
                    self.lineEdit_timeStart.setText("1999")  # 起始年份
                    QtWidgets.QApplication.processEvents()  # 刷新界面

            # 下载并显示二维码图片
            image_url = "http://xfxuezhang.cn/web/share/donate/yf.png"
            response = requests.get(image_url, timeout=10)  # 设置10秒超时
            if response.status_code == 200:
                self.label_yf.setAlignment(Qt.AlignCenter)  # 居中对齐
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)  # 从响应内容加载图片
                scaled_pixmap = pixmap.scaled(
                    self.label_yf.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                )  # 缩放图片以适应标签大小
                self.label_yf.setPixmap(scaled_pixmap)  # 设置图片到标签
            else:
                self.label_yf.setText("图片URL未找到")
        except Exception as e:
            print(f"UI设置错误: {e}")
            self._label_debug(f"UI设置错误: {e}")

    def Start_Run(self):
        """启动爬取线程
        
        初始化文章计数并启动主爬取线程，与 WeChat.py 中的信号连接一致。
        """
        self.total_articles = 0  # 重置文章总数
        process_thread = threading.Thread(target=self._process, daemon=True)  # 创建守护线程
        process_thread.start()  # 启动线程
        self.thread_list.append(process_thread)  # 添加到线程列表

    def Stop_Run(self):
        """停止爬取线程
        
        尝试终止所有运行中的线程并重置变量，与 WeChat.py 中的信号连接一致。
        """
        try:
            for _ in range(2):  # 尝试终止最多两个线程
                if self.thread_list:
                    self._stop_thread(self.thread_list.pop())  # 终止并移除线程
            self._init_variables()  # 重置变量
            self._label_debug("终止成功!")
            print("终止成功!")
        except Exception as e:
            self._label_debug("终止失败!")
            print(f"停止失败: {e}")

    def Start_Run_2(self):
        """启动关键词搜索模式
        
        创建存储目录并启动关键词搜索爬取线程，与 WeChat.py 中的信号连接一致。
        """
        Path(self.root_path).mkdir(exist_ok=True)  # 创建存储目录（如果不存在）
        self.keyword_search_mode = 1  # 启用关键词搜索模式
        self.total_articles = 0  # 重置文章总数
        process_thread = threading.Thread(target=self._process, daemon=True)
        process_thread.start()
        self.thread_list.append(process_thread)

    def Stop_Run_2(self):
        """停止关键词搜索模式
        
        关闭关键词搜索模式并终止相关线程，与 WeChat.py 中的信号连接一致。
        """
        try:
            self.keyword_search_mode = 0  # 关闭关键词搜索模式
            for _ in range(2):
                if self.thread_list:
                    self._stop_thread(self.thread_list.pop())
            self._init_variables()
            self._label_debug("终止成功!")
            print("终止成功!")
        except Exception as e:
            self._label_debug("终止失败!")
            print(f"停止失败: {e}")

    def _check_config(self):
        """检查并初始化配置文件
        
        检查 conf.ini 文件是否存在，加载或创建初始配置。
        
        Returns:
            int: 1 表示从现有配置恢复，0 表示新建配置
        """
        self.config = configparser.ConfigParser()  # 创建配置解析器
        self.config_path = os.path.join(self.init_path, "conf.ini")  # 配置文件路径
        if os.path.exists(self.config_path):  # 如果配置文件存在
            self.config.read(self.config_path, encoding="utf-8")  # 读取配置
            resume = dict(self.config["resume"])  # 获取 resume 部分
            self.root_path = resume["rootpath"]  # 存储路径
            self.page_num = int(resume["pagenum"])  # 页码
            self.link_buffer_count = int(resume["linkbuf_cnt"])  # 链接计数
            self.download_count = int(resume["download_cnt"])  # 下载计数
            self.total_articles = int(resume["total_articles"])  # 文章总数
            print(f"加载配置: {self.root_path}, {self.page_num}, {self.total_articles}")
            return 1
        else:  # 如果配置文件不存在
            with open(self.config_path, "w", encoding="utf-8") as f:
                self.config.add_section("resume")  # 添加 resume 部分
                self.config.set("resume", "rootpath", self.init_path)  # 设置默认路径
                self.config.set("resume", "pagenum", "0")  # 默认页码
                self.config.set("resume", "linkbuf_cnt", "0")  # 默认链接计数
                self.config.set("resume", "download_cnt", "0")  # 默认下载计数
                self.config.set("resume", "total_articles", "0")  # 默认文章总数
                self.config.write(f)  # 写入配置文件
            return 0

    def _process(self):
        """主爬取流程
        
        根据界面输入执行公众号文章爬取或关键词搜索。
        """
        try:
            # 从界面获取输入参数
            username = self.LineEdit_user.text()  # 用户名
            password = self.LineEdit_pwd.text()  # 密码
            query_name = self.LineEdit_target.text()  # 目标公众号
            self.time_gap = int(self.LineEdit_timegap.text() or 10)  # 爬取间隔，默认为10秒
            self.time_start = int(self.lineEdit_timeStart.text() or 1999)  # 起始年份
            self.time_end = int(self.lineEdit_timeEnd.text() or self.year_now + 1)  # 结束年份
            self.keyword = self.lineEdit_keyword.text()  # 关键词

            # 如果勾选保存选项且密码不为空，则保存登录信息
            if self.checkBox.isChecked() and password:
                login_data = {
                    "target": query_name,
                    "user": username,
                    "pwd": password,
                    "timegap": self.time_gap,
                }
                with open(os.path.join(self.init_path, "login.json"), "w") as file:
                    json.dump(login_data, file)

            # 登录并获取 token 和 cookies
            token, cookies = self._login(username, password)
            self._add_cookies(cookies)  # 添加 cookies 到会话
            if self.keyword_search_mode == 1:  # 关键词搜索模式
                self.keyword_2 = self.lineEdit_keyword_2.text()
                self._keyword_search(token, self.keyword_2)
            else:  # 公众号模式
                fakeid, nickname = self._get_wechat_subscription(token, query_name)
                if not self.is_resume:  # 如果不是恢复模式，创建新目录
                    index_count = 0
                    while True:
                        try:
                            self.root_path = os.path.join(
                                self.init_path, f"spider-{index_count}", nickname
                            )
                            os.makedirs(self.root_path, exist_ok=True)
                            self.config.set("resume", "rootpath", self.root_path)
                            with open(self.config_path, "w", encoding="utf-8") as f:
                                self.config.write(f)
                            break
                        except FileExistsError:
                            index_count += 1  # 如果目录已存在，尝试下一个编号
                self._get_articles(token, fakeid)  # 获取文章
        except Exception as e:
            self._label_debug(f"处理错误: {e}")
            print(f"处理错误: {e}")

    def _init_url_json(self):
        """初始化URL JSON文件
        
        创建或重置存储文章信息的 url.json 文件。
        """
        self.url_json_path = os.path.join(self.init_path, "url.json")  # JSON 文件路径
        if os.path.exists(self.url_json_path) and not self.is_resume:  # 如果需要重置
            os.remove(self.url_json_path)  # 删除现有文件
        if not os.path.exists(self.url_json_path):  # 如果文件不存在
            with open(self.url_json_path, "w") as f:
                json.dump([], f)  # 创建空数组
        with open(self.url_json_path, "r") as f:
            self.json_data = json.load(f)  # 读取 JSON 数据
        self.json_data_len = len(self.json_data)  # 记录初始长度

    def _update_url_json(self, data):
        """更新URL JSON文件
        
        向 url.json 中追加一条文章记录。
        
        Args:
            data (dict): 包含文章标题、链接和图片的信息
        """
        self.json_data.append(data)  # 添加新记录
        with open(self.url_json_path, "w") as f:
            json.dump(self.json_data, f)  # 写入文件

    def _login(self, username, password):
        """登录微信并获取token和cookies
        
        尝试使用本地 cookie 登录，若失败则打开浏览器要求手动登录。
        
        Args:
            username (str): 登录用户名
            password (str): 登录密码
        
        Returns:
            tuple: (token, cookies) - 登录令牌和 cookies 列表
        """
        try:
            cookie_file = os.path.join(self.init_path, "cookie.json")  # cookie 文件路径
            if os.path.exists(cookie_file):  # 如果存在 cookie 文件
                with open(cookie_file, "r") as f:
                    data = json.load(f)[0]  # 读取第一个记录
                cookies = data["COOKIES"]
                token = data["TOKEN"]
                if cookies and token:  # 如果 cookie 和 token 有效
                    self._label_debug("cookie.json读取成功")
                    self._add_cookies(cookies)
                    response = self.session.get(
                        f"https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token={token}",
                        timeout=(30, 60),  # 连接超时30秒，读取超时60秒
                    )
                    if "登陆" not in response.text:  # 检查是否需要重新登录
                        self._label_debug("cookie有效，无需浏览器登录")
                        return token, cookies
        except Exception as e:
            self._label_debug("cookie无效或缺失")

        # 如果 cookie 无效，启动浏览器进行手动登录
        self._label_debug("正在打开浏览器，请稍等")
        options = Options()
        options.add_argument("--incognito")  # 隐身模式
        options.add_argument("--disable-blink-features=AutomationControlled")  # 隐藏自动化特征
        browser = webdriver.Chrome(
            options=options, service=Service(ChromeDriverManager().install())
        )  # 自动下载并使用 ChromeDriver
        browser.maximize_window()  # 最大化窗口
        browser.get("https://mp.weixin.qq.com")  # 打开微信公众平台
        browser.implicitly_wait(60)  # 隐式等待60秒

        pyautogui.alert(title="请手动完成登录", text="完成登录后，点击确认!", button="确认")  # 弹出提示
        WebDriverWait(browser, 600, 0.5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".weui-desktop-account__info"))
        )  # 等待登录成功，最多10分钟
        self._label_debug("登录成功")
        token = re.search(r"token=([^&]+)", browser.current_url).group(1)  # 从 URL 提取 token
        cookies = browser.get_cookies()  # 获取 cookies
        with open(cookie_file, "w") as f:  # 保存到本地
            json.dump([{"COOKIES": cookies, "TOKEN": token}], f)
        browser.quit()  # 关闭浏览器
        return token, cookies

    def _add_cookies(self, cookies):
        """将cookies添加到session
        
        将从浏览器获取的 cookies 添加到 HTTP 会话中。
        
        Args:
            cookies (list): cookies 列表，每个元素为字典
        """
        cookie_jar = requests.cookies.RequestsCookieJar()  # 创建 cookie 容器
        for cookie in cookies:
            cookie_jar.set(cookie["name"], cookie["value"])  # 设置 cookie
        cookie_jar.set("wxtokenkey", "777")  # 设置 cookie
        cookie_jar.set("payforreadsn", "EXPIRED")  # 设置 cookie
        self.session.cookies.update(cookie_jar)  # 更新会话 cookies

    def _keyword_search(self, token, keyword):
        """按关键词搜索文章
        
        根据关键词搜索微信文章并保存结果。
        
        Args:
            token (str): 登录令牌
            keyword (str): 搜索关键词
        """
        self.url_buffer = []  # 存储文章链接
        self.title_buffer = []  # 存储文章标题
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Host": "mp.weixin.qq.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "Referer": f"https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&share=1&lang=zh_CN&token={token}",
        }  # 设置请求头
        url = "https://mp.weixin.qq.com/cgi-bin/operate_appmsg?sub=check_appmsg_copyright_stat"
        data = {
            "token": token,
            "lang": "zh_CN",
            "f": "json",
            "ajax": 1,
            "random": random.uniform(0, 1),  # 随机数防缓存
            "url": keyword,
            "allow_reprint": 0,
            "begin": 0,
            "count": 10,  # 每页10条
        }
        response = self.session.post(url, data=data, headers=headers).json()  # 发送初始请求
        total = response["total"]  # 总文章数
        total_pages = ceil(total / 10)  # 计算总页数

        table_index = 0  # 表格行索引
        for i in range(total_pages):
            data["begin"] = i * 10  # 设置分页起始位置
            data["random"] = random.uniform(0, 1)
            response = self.session.post(url, data=data, headers=headers).json()
            for j, item in enumerate(response["list"]):  # 遍历每页文章
                self.url_buffer.append(item["url"])
                self.title_buffer.append(item["title"])
                self._update_table(table_index, item["title"], item["url"])  # 更新界面表格
                table_index += 1
                self.total_articles += 1
                self._save_to_file(item["title"], item["url"], "")  # 保存到文件
            self._get_content(self.title_buffer, self.url_buffer)  # 下载内容
            self.url_buffer.clear()  # 清空缓冲区
            self.title_buffer.clear()

    def _get_wechat_subscription(self, token, query):
        """获取微信公众号信息
        
        根据公众号名称获取其 fakeid 和昵称。
        
        Args:
            token (str): 登录令牌
            query (str): 公众号名称
        
        Returns:
            tuple: (fakeid, nickname) - 公众号ID和昵称
        """
        if not query:  # 如果未提供公众号名称，使用默认值
            query = "xinhuashefabu1"
        url = f"https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={token}&lang=zh_CN&f=json&ajax=1&random=0.5182749224035845&query={query}&begin=0&count=5"
        response = self.session.get(url, headers=self.headers, timeout=(30, 60)).json()
        fakeid = response["list"][0]["fakeid"]  # 获取第一个匹配结果的ID
        nickname = response["list"][0]["nickname"]  # 获取昵称
        self._label_debug(f"公众号昵称: {nickname}")
        return fakeid, nickname

    def _get_articles(self, token, fakeid):
        """获取公众号文章
        
        获取指定公众号的所有文章并保存。
        
        Args:
            token (str): 登录令牌
            fakeid (str): 公众号ID
        """
        img_buffer = []  # 图片链接缓冲区
        total_buffer = []  # 已处理标题缓冲区，用于去重
        url = f"https://mp.weixin.qq.com/cgi-bin/appmsg?token={token}&lang=zh_CN&f=json&ajax=1&random={random.uniform(0, 1)}&action=list_ex&begin=0&count=5&query=&fakeid={fakeid}&type=9"
        response = self.session.get(url, headers=self.headers, timeout=(30, 60)).json()
        try:
            total_pages = ceil(int(response["app_msg_cnt"]) / 5)  # 计算总页数（每页5条）
            self.progressBar.setMaximum(total_pages)  # 设置进度条最大值
            QtWidgets.QApplication.processEvents()  # 刷新界面
        except Exception as e:
            self._label_debug(f"获取文章失败: {response['base_resp']['err_msg']}")
            return

        table_index = 0  # 表格行索引
        download_thread = threading.Thread(target=self._download_content, daemon=True)
        download_thread.start()  # 启动下载线程
        self.thread_list.append(download_thread)

        buffer_index = 0  # 缓冲区索引
        for i in range(total_pages):
            if self.is_resume:  # 如果是恢复模式，从上次页码继续
                i += self.page_num
            self._label_debug(f"第[{i + 1}/{total_pages}]页  url:{self.link_buffer_count}, article:{self.download_count}")
            begin = i * 5  # 计算分页起始位置
            url = f"https://mp.weixin.qq.com/cgi-bin/appmsg?token={token}&lang=zh_CN&f=json&ajax=1&random={random.uniform(0, 1)}&action=list_ex&begin={begin}&count=5&query=&fakeid={fakeid}&type=9"
            response = self._fetch_with_retry(url)  # 获取分页数据
            if not response:
                break
            try:
                app_msg_list = response.json()["app_msg_list"]  # 获取文章列表
            except Exception:
                self._label_debug("操作太频繁，5秒后重试")
                time.sleep(5)
                continue

            if not app_msg_list:  # 如果列表为空，结束抓取
                self._label_debug("抓取结束")
                break

            for j, item in enumerate(app_msg_list):  # 遍历每页文章
                if not self._should_process_item(item, total_buffer):  # 检查是否需要处理
                    continue
                self.title_buffer.append(item["title"])
                self.link_buffer.append(item["link"])
                img_buffer.append(item["cover"])
                total_buffer.append(item["title"])
                self._update_table(table_index, item["title"], item["link"])
                table_index += 1
                self.total_articles += 1
                self._save_to_file(item["title"], item["link"], item["cover"])
                buffer_index += j
            self._update_progress(i, total_pages)  # 更新进度
            time.sleep(self.time_gap)  # 每页间隔等待

        self._clear_label_debug()
        self._label_debug(">> 列表抓取结束!!! <<")
        self.download_end = 1  # 标记下载结束

    def _should_process_item(self, item, total_buffer):
        """检查是否应处理当前文章
        
        根据标题、关键词和时间范围判断是否处理该文章。
        
        Args:
            item (dict): 文章信息
            total_buffer (list): 已处理的标题列表
        
        Returns:
            bool: True 表示需要处理，False 表示跳过
        """
        article_time = int(time.strftime("%Y", time.localtime(int(item["update_time"]))))
        if item["title"] in total_buffer:
            self._label_debug("文章已存在，跳过")
            return False
        if self.keyword and self.keyword not in item["title"]:
            self._label_debug(f"不匹配关键词[{self.keyword}]，跳过")
            return False
        if self.time_start > article_time:
            self._label_debug(f"时间[{article_time}]不在范围[{self.time_start}-{self.time_end}]内，跳过")
            return False
        if article_time > self.time_end:
            self._label_debug("达到结束时间，退出")
            self.Stop_Run()
            return False
        return True

    def _update_table(self, index, title, url):
        """更新结果表格
        
        在界面表格中添加一行文章信息。
        
        Args:
            index (int): 表格行索引
            title (str): 文章标题
            url (str): 文章链接
        """
        table_count = self.tableWidget_result.rowCount()
        if index >= table_count:  # 如果需要新行
            self.tableWidget_result.insertRow(table_count)
        self.tableWidget_result.setItem(index, 0, QtWidgets.QTableWidgetItem(title))
        self.tableWidget_result.setItem(index, 1, QtWidgets.QTableWidgetItem(url))

    def _save_to_file(self, title, link, img):
        """保存文章信息到文件
        
        将文章信息保存到 spider.txt 和 url.json 中。
        
        Args:
            title (str): 文章标题
            link (str): 文章链接
            img (str): 文章封面图链接
        """
        os.makedirs(self.root_path, exist_ok=True)  # 确保目录存在
        data = {"Title": title, "Link": link, "Img": img}
        self._update_url_json(data)  # 更新 JSON 文件
        with open(os.path.join(self.root_path, "spider.txt"), "a+", encoding="utf-8") as f:
            f.write(
                f"{'*' * 60}\n【{self.total_articles}】\n  Title: {title}\n  Link: {link}\n  Img: {img}\n\n"
            )  # 写入文本文件
        self._label_debug(f">> 第{self.total_articles}条写入完成：{title}")
        self.config.set("resume", "total_articles", str(self.total_articles))
        with open(self.config_path, "w", encoding="utf-8") as f:
            self.config.write(f)  # 更新配置文件

    def _fetch_with_retry(self, url, retries=3):
        """带重试的网络请求
        
        对网络请求进行重试机制以处理连接失败。
        
        Args:
            url (str): 请求的 URL
            retries (int): 最大重试次数，默认为3
        
        Returns:
            dict or None: JSON 响应数据，或 None 如果所有重试失败
        """
        for _ in range(retries):
            try:
                
                resp = self.session.get(url, headers=self.headers, timeout=(30, 60))
                return resp
            except Exception as e:
                # print(url, resp.text)
                self._label_debug(f"连接出错，稍等2秒: {e}")
                time.sleep(2)
        return None

    def _update_progress(self, current_page, total_pages):
        """更新进度信息
        
        更新界面进度显示和配置文件中的计数。
        
        Args:
            current_page (int): 当前页码
            total_pages (int): 总页数
        """
        self.link_buffer_count = (
            len(self.link_buffer) + self.json_data_len if self.is_resume else len(self.link_buffer)
        )  # 计算链接总数
        self.config.set("resume", "linkbuf_cnt", str(self.link_buffer_count))
        self.config.set("resume", "pagenum", str(current_page))
        with open(self.config_path, "w", encoding="utf-8") as f:
            self.config.write(f)
        self.label_total_Page.setText(
            f"第[{current_page + 1}/{total_pages}]页  linkbuf_cnt:{self.link_buffer_count}, download_cnt:{self.download_count}"
        )  # 更新界面显示

    def _get_content(self, title_buffer, link_buffer):
        """下载文章内容
        
        下载并保存文章的文本、图片、HTML 和评论。
        
        Args:
            title_buffer (list or str): 文章标题或标题列表
            link_buffer (list or str): 文章链接或链接列表
        """
        length = len(title_buffer) if self.keyword_search_mode == 1 else 1
        for index in range(length):
            title = re.sub(r'[|/<>:*?"]', "_", title_buffer[index] if self.keyword_search_mode == 1 else title_buffer)
            filepath = os.path.join(self.root_path, title)
            os.makedirs(filepath, exist_ok=True)  # 创建文章目录
            os.chdir(filepath)  # 切换到文章目录

            url = link_buffer[index] if self.keyword_search_mode == 1 else link_buffer
            html = self._fetch_with_retry(url)  # 获取文章页面
            if not html: continue

            soup = BeautifulSoup(html.text, "lxml")  # 解析 HTML
            # print(soup)
            self._save_article_text(soup, title)  # 保存文本
            self._save_article_images(soup, title)  # 保存图片
            self._save_html(soup, title)  # 保存 HTML
            self._save_comments(url, title)  # 保存评论

            if self.keyword_search_mode == 1:  # 关键词模式下每篇文章间隔等待
                self._label_debug(f">> 休息 {self.time_gap} 秒")
                time.sleep(self.time_gap)

    def _save_article_text(self, soup, title):
        """保存文章文本
        
        提取并保存文章的正文内容到文本文件。
        
        Args:
            soup (BeautifulSoup): 解析后的 HTML 对象
            title (str): 文章标题
        """
        try:
            article = soup.find(class_="rich_media_content").find_all("p")  # 查找正文段落
            with open(f"{title}.txt", "a+", encoding="utf-8") as f:
                for p in article:
                    text = p.get_text()
                    if text:  # 如果段落有文本内容
                        f.write(f"{text}\n")
            self._label_debug(">> 保存文档 - 完毕!")
        except Exception as e:
            self._label_debug(f"未匹配到文字: {e}")

    def _save_article_images(self, soup, title):
        """保存文章图片
        
        下载并保存文章中的所有图片。
        
        Args:
            soup (BeautifulSoup): 解析后的 HTML 对象
            title (str): 文章标题
        """
        try:
            img_urls = soup.find(class_="rich_media_content").find_all("img")  # 查找所有图片
            for i, img in enumerate(img_urls):
                for _ in range(3):  # 每张图片尝试3次下载
                    try:
                        response = self.session.get(img["data-src"], timeout=(30, 60))
                        with open(f"{i}.jpeg", "ab+") as f:
                            f.write(response.content)
                        break
                    except Exception as e:
                        self._label_debug(f"图片下载超时: {e}")
                else:
                    self._label_debug("放弃此图")  # 重试失败后放弃
            self._label_debug(f">> 保存图片{len(img_urls)}张 - 完毕!")
        except Exception as e:
            self._label_debug(f"未匹配到图片: {e}")

    def _save_html(self, soup, title):
        """保存HTML文件
        
        保存文章的完整 HTML 内容。
        
        Args:
            soup (BeautifulSoup): 解析后的 HTML 对象
            title (str): 文章标题
        """
        with open(f"{title}.html", "w", encoding="utf-8") as f:
            f.write(str(soup))
        self._label_debug(">> 保存html - 完毕!")

    def _save_comments(self, url, title):
        """保存文章评论
        
        获取并保存文章的评论到文件。
        
        Args:
            url (str): 文章链接
            title (str): 文章标题
        """
        comments = self._get_comments(url, self.wechat_uin, self.wechat_key)
        with open(f"{title}_comments.txt", "a+", encoding="utf-8") as f:
            f.write("\n".join(comments))
        self._label_debug(">> 保存评论 - 完毕!")

    def _get_comments(self, article_url, uin, key, offset=0):
        """获取文章评论
        
        从微信接口获取文章的评论内容。
        
        Args:
            article_url (str): 文章链接
            uin (str): 微信 UIN
            key (str): 微信 Key
            offset (int): 评论偏移量，默认为0
        
        Returns:
            list: 评论列表，每个元素为“昵称: 内容”格式
        """
        comments = []
        if not uin or not key:  # 如果缺少 UIN 或 Key，返回空列表
            return comments
        biz = re.search(r"__biz=(.*?)&", article_url).group(1)  # 提取公众号标识
        comment_id = self._get_comment_id(article_url)  # 获取评论ID
        if not comment_id:
            return comments

        url = "https://mp.weixin.qq.com/mp/appmsg_comment?"
        params = {
            "action": "getcomment",
            "comment_id": comment_id,
            "uin": uin,
            "key": key,
            "__biz": biz,
            "offset": str(offset),
            "limit": "100",  # 每次获取100条评论
            "f": "json",
        }
        try:
            response = self.session.get(url, params=params).json()
            if response.get("elected_comment_total_cnt"):  # 如果有精选评论
                for item in response["elected_comment"]:
                    comments.append(f"{item['nick_name']}: {item['content']}")
        except Exception:
            pass  # 忽略评论获取失败
        return comments

    def _get_comment_id(self, article_url):
        """获取文章评论ID
        
        从文章页面提取评论ID。
        
        Args:
            article_url (str): 文章链接
        
        Returns:
            str or None: 评论ID，或 None 如果提取失败
        """
        try:
            response = requests.get(article_url).text
            pattern = re.compile(r'comment_id\s*=\s*"(?P<id>\d+)"')
            return pattern.search(response)["id"]
        except Exception:
            return None

    def _download_content(self):
        """下载内容线程
        
        持续检查缓冲区并下载文章内容，直到任务完成。
        """
        while True:
            try:
                if self.download_count < self.link_buffer_count:  # 如果有待下载的内容
                    if self.is_resume:  # 恢复模式下从 JSON 文件读取
                        self.json_data = json.load(open(self.url_json_path, "r"))
                        self._get_content(
                            self.json_data[self.download_count]["Title"],
                            self.json_data[self.download_count]["Link"],
                        )
                    else:  # 正常模式下从缓冲区读取
                        self._get_content(
                            self.title_buffer[self.download_count],
                            self.link_buffer[self.download_count],
                        )
                    self.download_count += 1
                    self.config.set("resume", "download_cnt", str(self.download_count))
                    with open(self.config_path, "w", encoding="utf-8") as f:
                        self.config.write(f)
                elif self.download_count >= self.link_buffer_count and self.download_end:
                    self._clear_label_debug()
                    self._label_debug(">> 程序结束, 欢迎再用!!! <<")
                    break  # 下载完成，退出循环
                elif self.download_count == self.link_buffer_count and not self.download_end:
                    time.sleep(2)  # 等待更多内容
            except Exception as e:
                self._label_debug(f"下载内容错误: {e}")

    def _async_raise(self, tid, exc_type):
        """强制抛出异常以终止线程
        
        使用 ctypes 向指定线程抛出异常。
        
        Args:
            tid (int): 线程ID
            exc_type (type): 要抛出的异常类型
        
        Raises:
            ValueError: 如果线程ID无效
            SystemError: 如果线程状态设置失败
        """
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exc_type):
            exc_type = type(exc_type)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
        if res == 0:
            raise ValueError("无效线程ID")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("线程状态设置失败")

    def _stop_thread(self, thread):
        """停止指定线程
        
        调用 _async_raise 强制终止线程。
        
        Args:
            thread (threading.Thread): 要终止的线程对象
        """
        self._async_raise(thread.ident, SystemExit)


def main():
    """程序入口
    
    初始化 PyQt5 应用程序并显示主窗口。
    """
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
