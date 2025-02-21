import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from datetime import datetime

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", color="grey", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self["fg"]

        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.delete(0, tk.END)
        self.insert(0, self.placeholder)
        self.config(fg=self.placeholder_color)

    def on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg=self.default_fg_color)

    def on_focus_out(self, event):
        if not self.get():
            self.put_placeholder()
    
    def get(self):
        content = super().get()
        if content == self.placeholder:
            return ""
        else:
            return content.strip()
        
class Ui_MainWindow:
    def setupUi(self, root):
        root.title("微信公众号文章 by 小锋学长")
        root.geometry("800x700")  # 固定窗口大小
        root.minsize(800, 700)    # 最小尺寸与初始尺寸相同
        root.maxsize(800, 700)    # 最大尺寸与初始尺寸相同
        root.resizable(False, False)  # 禁止窗口缩放（宽度和高度都不可调整）
        root.configure(bg="#f0f0f0")
        try:
            root.iconbitmap("../../icon.jpg")
        except:
            pass

        self.header_font = tkFont.Font(family="华文楷体", size=12, weight="bold")
        self.label_font = tkFont.Font(family="宋体", size=10)
        self.entry_font = tkFont.Font(family="宋体", size=12)  # 保持稍大的字体增加高度

        self.tab_control = ttk.Notebook(root)
        self.tab_control.grid(row=0, column=0, sticky='nsew')

        # 配置窗口权重，使内容随窗口大小调整
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='  公众号搜文章  ')
        self.tab_control.add(self.tab2, text='  关键词搜文章  ')

        self.setup_tab1()
        self.setup_tab2()

    def setup_tab1(self):
        # 顶部标题区域
        top_frame = tk.Frame(self.tab1, bg="#f0f0f0")
        top_frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        self.label_head = tk.Label(top_frame, text="****************************************************************************\n* 程序原理: 通过selenium登录获取token和cookie，再自动爬取和下载\n* 使用前提: 申请一个微信公众号 (https://mp.weixin.qq.com)\n开源链接: https://github.com/1061700625/WeChat_Article\n                         Copyright © SXF  本软件禁止一切形式的商业活动\n****************************************************************************", 
                                   font=self.header_font, justify="left", bg="#e0f7fa", fg="#006064", padx=10, pady=10, relief="flat", wraplength=780)
        self.label_head.grid(row=0, column=0, sticky='nsew')

        # 配置顶部框架权重
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_rowconfigure(0, weight=1)

        # 中间区域：表单 + 按钮（使用 grid 布局）
        middle_frame = tk.Frame(self.tab1, bg="#f0f0f0")
        middle_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        # 左侧表单区域（垂直排列）
        form_frame = tk.Frame(middle_frame, bg="#f0f0f0")
        form_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))

        labels = ["目标公众号英文名", "个人公众号账号", "个人公众号密码", "查询间隔(s)", "微信uin和key", "时间范围(年)"]
        placeholders = [
            "为空则默认新华社(xinhuashefabu1)",
            "为空则自动打开页面后手动输入",
            "为空则自动打开页面后手动输入",
            "为空则默认为5s，一页约10条",
            "URL全复制进来，通过Fiddler抓包",
            ""
        ]
        self.entries = {}
        label_width = 15
        for i, (label, placeholder) in enumerate(zip(labels, placeholders)):
            tk.Label(form_frame, text=label, font=self.label_font, bg="#f0f0f0", width=label_width, anchor='w').grid(row=i, column=0, padx=5, pady=2, sticky='w')
            if label == "时间范围(年)":
                time_frame = tk.Frame(form_frame, bg="#f0f0f0")
                time_frame.grid(row=i, column=1, sticky='w', pady=2)
                self.entries["timeStart"] = PlaceholderEntry(time_frame, placeholder="1999", width=8, font=self.entry_font)
                self.entries["timeStart"].grid(row=0, column=0, padx=2, pady=2)
                tk.Label(time_frame, text="-", bg="#f0f0f0").grid(row=0, column=1, padx=2)
                self.entries["timeEnd"] = PlaceholderEntry(time_frame, placeholder=str(datetime.now().year), width=8, font=self.entry_font)
                self.entries["timeEnd"].grid(row=0, column=2, padx=2, pady=2)
                tk.Label(time_frame, text="关键词", font=self.label_font, bg="#f0f0f0", width=8, anchor='w').grid(row=0, column=3, padx=5, pady=2, sticky='w')
                self.entries["keyword"] = tk.Entry(time_frame, width=20, font=self.entry_font)
                self.entries["keyword"].grid(row=0, column=4, padx=2, pady=2)
            else:
                self.entries[label] = PlaceholderEntry(form_frame, placeholder=placeholder, width=60, font=self.entry_font)
                self.entries[label].grid(row=i, column=1, padx=5, pady=2, sticky='w')
                if label == "个人公众号密码":
                    self.entries[label].config(show='*')
                ToolTip(self.entries[label], placeholder)

        # 配置表单框架权重
        form_frame.grid_columnconfigure(1, weight=1)
        for i in range(len(labels)):
            form_frame.grid_rowconfigure(i, weight=0)

        # 右侧按钮区域（垂直排列）
        button_frame = tk.Frame(middle_frame, bg="#f0f0f0")
        button_frame.grid(row=0, column=1, sticky='ns', padx=5)

        self.pushButton_start = tk.Button(button_frame, text="启动 (*^▽^*)", command=self.Start_Run, bg="#4caf50", fg="white", font=self.label_font, relief="flat", padx=10, pady=5)
        self.pushButton_start.grid(row=0, column=0, pady=5, sticky='ew')
        self.CheckVar = tk.IntVar()  # 创建变量
        self.checkBox = tk.Checkbutton(button_frame, text="记住密码", font=self.label_font, bg="#f0f0f0", variable=self.CheckVar)
        self.checkBox.grid(row=1, column=0, pady=5, sticky='w')
        self.pushButton_stop = tk.Button(button_frame, text="终止 ￣へ￣", command=self.Stop_Run, bg="#f44336", fg="white", font=self.label_font, relief="flat", padx=10, pady=5)
        self.pushButton_stop.grid(row=2, column=0, pady=5, sticky='ew')

        # 配置按钮框架权重
        button_frame.grid_rowconfigure((0, 2), weight=0)
        button_frame.grid_rowconfigure(1, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)

        # 底部区域：进度条 + 表格 + 调试信息
        bottom_frame = tk.Frame(self.tab1, bg="#f0f0f0")
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        self.progressBar = ttk.Progressbar(bottom_frame, orient='horizontal', mode='determinate', maximum=100)
        self.progressBar.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 5))

        table_notes_frame = tk.Frame(bottom_frame, bg="#f0f0f0")
        table_notes_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.tableWidget_result = ttk.Treeview(table_notes_frame, columns=('Title', 'URL'), show='headings', height=10)
        self.tableWidget_result.heading('Title', text='标题')
        self.tableWidget_result.heading('URL', text='链接')
        self.tableWidget_result.column('Title', width=300)  # 确保不超过窗口
        self.tableWidget_result.column('URL', width=200)
        self.tableWidget_result.grid(row=0, column=0, sticky='nsew', padx=(0, 5))

        self.label_notes = tk.Label(table_notes_frame, text="调试信息窗口", font=self.label_font, bg="#fff3e0", fg="#e65100", relief="sunken", anchor='nw', justify='left', wraplength=300, width=35, height=10, padx=5, pady=5)
        self.label_notes.grid(row=0, column=1, sticky='nsew', padx=5)

        # 配置底部框架权重
        bottom_frame.grid_rowconfigure(1, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=1)
        table_notes_frame.grid_columnconfigure(0, weight=3)  # 表格占更多空间
        table_notes_frame.grid_columnconfigure(1, weight=1)  # 调试窗口占少部分
        table_notes_frame.grid_rowconfigure(0, weight=1)

        # 配置主窗口权重
        self.tab1.grid_rowconfigure((0, 1, 2), weight=0)
        self.tab1.grid_columnconfigure(0, weight=3)  # 表单和表格占更多
        self.tab1.grid_columnconfigure(1, weight=1)  # 按钮占少部分

    def setup_tab2(self):
        # 顶部标题区域
        top_frame = tk.Frame(self.tab2, bg="#f0f0f0")
        top_frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        self.label_head_2 = tk.Label(top_frame, text="****************************************************************************************************\n* Demo 说明: \n先在“公众号搜文章”页填完整信息，再在本页填入关键词，点击“启动”即可\n                         Copyright © SXF  本软件禁止一切形式的商业活动\n****************************************************************************************************", 
                                     font=self.header_font, justify="left", bg="#e0f7fa", fg="#006064", padx=10, pady=10, relief="flat", wraplength=780)
        self.label_head_2.grid(row=0, column=0, sticky='nsew')

        # 配置顶部框架权重
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_rowconfigure(0, weight=1)

        # 中间区域：关键词 + 按钮
        middle_frame = tk.Frame(self.tab2, bg="#f0f0f0")
        middle_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        content_frame = tk.Frame(middle_frame, bg="#f0f0f0")
        content_frame.grid(row=0, column=0, sticky='w', pady=10)
        tk.Label(content_frame, text="关键词", font=self.label_font, bg="#f0f0f0", width=10, anchor='w').grid(row=0, column=0, padx=5, pady=2, sticky='w')  # 减少标签宽度到100
        self.lineEdit_keyword_2 = tk.Entry(content_frame, width=35, font=self.entry_font)  # 保持35，确保不超过窗口
        self.lineEdit_keyword_2.grid(row=0, column=1, padx=5, pady=2, sticky='w')

        button_frame = tk.Frame(middle_frame, bg="#f0f0f0")
        button_frame.grid(row=0, column=1, sticky='e', pady=10)
        self.pushButton_start_2 = tk.Button(button_frame, text="启动 (*^▽^*)", command=self.Start_Run_2, bg="#4caf50", fg="white", font=self.label_font, relief="flat", padx=10, pady=5)
        self.pushButton_start_2.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.pushButton_stop_2 = tk.Button(button_frame, text="终止 ￣へ￣", command=self.Stop_Run_2, bg="#f44336", fg="white", font=self.label_font, relief="flat", padx=10, pady=5)
        self.pushButton_stop_2.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        # 配置中间框架权重
        middle_frame.grid_columnconfigure(0, weight=3)  # 关键词占更多
        middle_frame.grid_columnconfigure(1, weight=1)  # 按钮占少部分
        middle_frame.grid_rowconfigure(0, weight=1)

        # 配置主窗口权重
        self.tab2.grid_rowconfigure((0, 1), weight=0)
        self.tab2.grid_columnconfigure((0, 1), weight=1)

    def Start_Run(self):
        self.progressBar['value'] = 20
        self.label_notes.config(text="正在启动...\n请稍候...")

    def Stop_Run(self):
        self.progressBar['value'] = 0
        self.label_notes.config(text="已终止")

    def Start_Run_2(self):
        pass

    def Stop_Run_2(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    ui = Ui_MainWindow()
    ui.setupUi(root)
    root.mainloop()