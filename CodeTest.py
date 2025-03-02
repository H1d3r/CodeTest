# -*- coding:UTF-8 -*-
from tkinter import ttk,messagebox,scrolledtext,Toplevel,Tk,Menu,Frame,Button,Label,Entry,Text,Spinbox,Scrollbar,Checkbutton,LabelFrame,IntVar,filedialog
from tkinter import HORIZONTAL,BOTH,INSERT,END,S,W,E,N,TOP,BOTTOM,X,LEFT,NONE,RIGHT,Y
from ClassCongregation import ysoserial_payload,Sql_scan,TextRedirector,color,open_html,FrameProgress,seconds2hms,LoadCMD,delText,random_name
from concurrent.futures import ThreadPoolExecutor
from requests_toolbelt.utils import dump
from openpyxl import Workbook
import util.globalvar as GlobalVar
import prettytable as pt
import os,sys,time,socket,datetime
import importlib,glob,requests,binascii,re
import threading,math,json,base64
import urllib3
import inspect
import ctypes
# 支持TLSv1.0和TLSv1.1
os.environ['COMPOSE_TLS_VERSION'] = "TLSv1_2"
# 去除错误警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 调用api设置成由应用程序缩放
try:
    # version >= win 8.1
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    # version win 8.0 or less
    ctypes.windll.user32.SetProcessDPIAware()
#调用api获得当前的缩放因子
try:
    # version >= win 8
    scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
except:
    # version win 7 or less
    scaleFactor = 125
#主界面类
class MyGUI:
    # POC界面当前加载的对象
    vuln = None
    # 填充线程列表,创建多个存储POC脚本的界面, 默认为1, 2, 3, 4
    threadList = []
    # 线程锁
    threadLock = threading.Lock()
    # poc下的脚本文件列表
    scripts = []
    # poc首字母
    uppers = []
    # 用于wait_running函数
    wait_index = 0
    # 选中的checkbutton,代表执行的POC脚本名称
    Checkbutton_text = ''
    # 保存多个checkbutton关联的变量
    var = {}
    # 用于生成checkbutton处的定位
    row = 1
    # 当前脚本名称
    vul_name = ''
    # 当前结果文件
    wb = None
    # excel表格
    ws = None
    # 批量结果保存开关
    wbswitch = ''
    # 屏幕存储
    screens = []
    # 对象属性参数字典
    frms = []
    # 初始化窗体对象
    def __init__(self):
        self.root = Tk()
        self.root.tk.call('tk', 'scaling', scaleFactor / 75)
        self.root.iconbitmap('python.ico')
        # 设置title
        self.title = self.root.title('POC检测')
        # 设置窗体大小，1160x750是窗体大小，400+50是初始位置
        self.size = self.root.geometry('1160x750+400+50')
        # 不允许扩大
        # self.exchange = self.root.resizable(width=False, height=False)
        self.root.columnconfigure(0, weight=1)
        # 对象属性参数字典
        self.frms = self.__dict__
        # 创建顶级菜单
        self.menubar = Menu(self.root)
        # 创建一个菜单
        self.menubar_1 = Menu(self.root,tearoff=False)
        
        # 顶级菜单添加一个子菜单
        self.menubar1 = Menu(self.root,tearoff=False)
        self.menubar1.add_command(label = "项目根目录", command=lambda:LoadCMD('/'))
        self.menubar1.add_command(label = "POC目录", command=lambda:LoadCMD('/POC'))
        self.menubar1.add_command(label = "EXP目录", command=lambda:LoadCMD('/EXP'))
        self.menubar1.add_command(label = "Shell目录", command=lambda:LoadCMD('/execScripts'))
        self.menubar1.add_command(label = "Result目录", command=lambda:LoadCMD('/result'))
        self.menubar1.add_command(label = "Log目录", command=lambda:LoadCMD('/log'))
        self.menubar1.add_command(label = "Payload_html", command=lambda:LoadCMD('/payload_html'))
        self.menubar1.add_command(label = "字典目录", command=lambda:LoadCMD('/dict'))
        self.menubar.add_cascade(label = "打开文件", menu = self.menubar1)

        # 顶级菜单增加一个普通的命令菜单项
        self.menubar.add_command(label = "设置代理", command=lambda : myproxy.show())
        self.menubar.add_command(label = "免费代理池", command=lambda : my_proxy_pool.show())
        self.menubar.add_command(label = "全局配置文件", command=lambda:thread_it(CodeFile,**{
            'root': gui.root,
            'file_name': 'GlobSettings',
            'Logo': '1',
            'vuln_select': GlobalVar.get_value('settings_vuln'),
            'text': '',
            }))
        # 显示菜单
        self.root.config(menu = self.menubar)

    # 创造幕布
    def CreateFrm(self):
        self.frmTOP = Frame(self.root, width=1160 , height=35, bg='whitesmoke')
        self.frmPOC = Frame(self.root, width=1160 , height=700, bg='whitesmoke')
        self.frmSpace = Frame(self.root, width=1160 , height=700, bg='whitesmoke')
        self.frmEXP = Frame(self.root, width=1160 , height=700, bg='whitesmoke')
        self.frmCheck = Frame(self.root, width=1160 , height=700, bg='whitesmoke')
        self.frmNote = Frame(self.root, width=1160 , height=700, bg='whitesmoke')
        self.frmDb = Frame(self.root, width=1160 , height=700, bg='whitesmoke')
        self.frmDebug = Frame(self.root, width=1160 , height=700, bg='whitesmoke')
        self.frmTerlog = Frame(self.root, width=1160 , height=700, bg='whitesmoke')
        self.frmtools = Frame(self.root, width=1160 , height=700, bg='whitesmoke')
        self.frmthread = Frame(self.root, width=1160 , height=700, bg='whitesmoke')
        
        # 界面列表
        MyGUI.screens.append(self.frmPOC)
        MyGUI.screens.append(self.frmSpace)
        MyGUI.screens.append(self.frmEXP)
        MyGUI.screens.append(self.frmCheck)
        MyGUI.screens.append(self.frmNote)
        MyGUI.screens.append(self.frmDb)
        MyGUI.screens.append(self.frmDebug)
        MyGUI.screens.append(self.frmTerlog)
        MyGUI.screens.append(self.frmtools)
        MyGUI.screens.append(self.frmthread)

        # 界面初始化
        self.frmTOP.pack(side=TOP, expand=0, fill=X)
        self.frmPOC.pack(side=BOTTOM, expand=1, fill=BOTH)

        # 创建按钮
        self.frmTOPButton1 = Button(self.frmTOP, text='信息收集', width = 10, command=lambda :switchscreen(self.frmPOC))
        self.frmTOPButton2 = Button(self.frmTOP, text='资产空间', width = 10, command=lambda :switchscreen(self.frmSpace))
        self.frmTOPButton3 = Button(self.frmTOP, text='漏洞扫描', width = 10, command=lambda :switchscreen(self.frmEXP))
        self.frmTOPButton4 = Button(self.frmTOP, text='漏洞测试', width = 10, command=lambda :switchscreen(self.frmCheck))
        self.frmTOPButton5 = Button(self.frmTOP, text='漏洞仓库', width = 10, command=lambda :switchscreen(self.frmDb))
        #self.frmTOPButton6 = Button(self.frmTOP, text='漏洞工具', width = 10, command=lambda :switchscreen(self.frmtools))
        self.frmTOPButton7 = Button(self.frmTOP, text='威胁分析', width = 10, command=lambda :switchscreen(self.frmthread))
        self.frmTOPButton8 = Button(self.frmTOP, text='漏洞笔记', width = 10, command=lambda :switchscreen(self.frmNote))
        self.frmTOPButton9 = Button(self.frmTOP, text='异常日志', width = 10, command=lambda :switchscreen(self.frmDebug))

        # 一、pack布局
        # side=LEFT（靠左对齐）
        # expand=1（允许扩大）
        # fill=BOTH（窗体占满整个窗口剩余的空间）
        # self.frmTOPButton1.pack(side=LEFT, expand=1, fill=BOTH)
        # self.frmTOPButton2.pack(side=LEFT, expand=1, fill=BOTH)
        # self.frmTOPButton3.pack(side=LEFT, expand=1, fill=BOTH)
        # self.frmTOPButton4.pack(side=LEFT, expand=1, fill=BOTH)
        # self.frmTOPButton5.pack(side=LEFT, expand=1, fill=BOTH)
        # self.frmTOPButton6.pack(side=LEFT, expand=1, fill=BOTH)
        # self.frmTOPButton7.pack(side=LEFT, expand=1, fill=BOTH)
        # self.frmTOPButton8.pack(side=LEFT, expand=1, fill=BOTH)
        # self.frmTOPButton9.pack(side=LEFT, expand=1, fill=BOTH)

        # 二、grid布局
        self.frmTOPButton1.grid(row=0, column=0, padx=1, pady=1)
        self.frmTOPButton2.grid(row=0, column=1, padx=1, pady=1)
        self.frmTOPButton3.grid(row=0, column=2, padx=1, pady=1)
        self.frmTOPButton4.grid(row=0, column=3, padx=1, pady=1)
        self.frmTOPButton5.grid(row=0, column=4, padx=1, pady=1)
        #self.frmTOPButton6.grid(row=0, column=5, padx=1, pady=1)
        self.frmTOPButton7.grid(row=0, column=6, padx=1, pady=1)
        self.frmTOPButton8.grid(row=0, column=7, padx=1, pady=1)
        self.frmTOPButton9.grid(row=0, column=8, padx=1, pady=1)

        # 定义frame
        # 此处 height 可控制按钮高度
        self.frmPOC_A = Frame(self.frmPOC, width=860, height=680, bg='whitesmoke')
        self.frmPOC_B = Frame(self.frmPOC, width=300, height=680, bg='whitesmoke')
        # pack定位
        self.frmPOC_A.pack(side=LEFT, expand=1, fill=BOTH)
        self.frmPOC_B.pack(side=RIGHT, expand=0, fill=Y)
        
        self.frmA = Frame(self.frmPOC_A, width=860, height=20,bg='white')
        self.frmB = Frame(self.frmPOC_A, width=860, height=580, bg='whitesmoke')
        self.frmC = Frame(self.frmPOC_A, width=860, height=40, bg='whitesmoke')
        self.frmE = Frame(self.frmPOC_B, width=300, height=40, bg='white')
        self.frmD = Frame(self.frmPOC_B, width=300, height=580, bg='whitesmoke')
        self.frmF = Frame(self.frmPOC_B, width=300, height=40, bg='white')
        
        self.frmA.pack(side=TOP, expand=0, fill=X)
        self.frmB.pack(side=TOP, expand=1, fill=BOTH)
        self.frmC.pack(side=TOP, expand=0, fill=X)
        
        # expand=0, fill=X 窗体不允许扩大,在X轴方向上填充
        self.frmE.pack(side=TOP, expand=0, fill=X)
        self.frmD.pack(side=TOP, expand=1, fill=BOTH)
        self.frmF.pack(side=TOP, expand=0, fill=X)
        
    # 创造第一象限
    def CreateFirst(self):
        # 目标框
        self.LabA = Label(self.frmA, text='目标')
        self.EntA = Entry(self.frmA, width='55', highlightcolor='red', highlightthickness=1, font=("consolas", 10))
        # 运行状态框
        self.LabA2 = Label(self.frmA, text='运行状态')
        self.TexA2 = Text(self.frmA, font=("consolas",10), width=2, height=1)
        # 批量导入文件
        self.ButtonA = Button(self.frmA, text='......', width=5, command=lambda :myurls.show())
        # 线程池数量
        self.LabA3 = Label(self.frmA, text='线程(默认10)')
        self.b1 = Spinbox(self.frmA, from_=1, to=10, wrap=True, width=3, font=("consolas",10), textvariable=Ent_A_Top_thread)

        # pack布局
        self.LabA.pack(side=LEFT, expand=0, fill=NONE)
        self.EntA.pack(side=LEFT, expand=1, fill=X)
        self.LabA2.pack(side=LEFT, expand=0, fill=NONE)
        self.TexA2.pack(side=LEFT, expand=0, fill=NONE)
        self.ButtonA.pack(side=LEFT, expand=0, fill=NONE)
        self.LabA3.pack(side=LEFT, expand=0, fill=NONE)
        self.b1.pack(side=LEFT, expand=0, fill=NONE)

        # grid布局
        # self.LabA.grid(row=0, column=0, padx=2, pady=2)
        # self.EntA.grid(row=0, column=1, padx=2, pady=2)
        # self.LabA2.grid(row=0, column=2, padx=2, pady=2)
        # self.TexA2.grid(row=0, column=3, padx=2, pady=2)
        # self.ButtonA.grid(row=0, column=4, padx=2, pady=2)
        # self.LabA3.grid(row=0, column=5, padx=2, pady=2)
        # self.b1.grid(row=0, column=6, padx=2, pady=2)
        # 锁定屏幕,不允许写入
        self.TexA2.configure(state="disabled")

    # 创造第二象限
    def CreateSecond(self):
        self.TexB = scrolledtext.ScrolledText(self.frmB, font=("consolas",9), width=104, height=31)
        self.TexB.pack(side=TOP, expand=1, fill=BOTH)
        self.frame_progress = FrameProgress(self.frmB, height=10, maximum=1000)
        self.frame_progress.pack(side=BOTTOM, expand=0, fill=X)

    #创造第三象限
    def CreateThird(self):
        self.ButtonC1 = Button(self.frmC, text='验 证', width = 10, command=lambda : self.thread_it(self.BugTest,**
        {
            'url' : self.EntA.get(),
            'pool' : int(Ent_A_Top_thread.get())
            }
        ))
        self.ButtonC2 = Button(self.frmC, text='终 止', width = 10, command=lambda:self.thread_it(self.stop_thread))
        self.ButtonC3 = Button(self.frmC, text='清空信息', width = 15, command=lambda : delText(gui.TexB))
        self.ButtonC4 = Button(self.frmC, text='重新载入当前POC', width = 15, command=ReLoad)
        self.ButtonC5 = Button(self.frmC, text='当前进程运行状态', width = 15, command=ShowPython)
        self.ButtonC6 = Button(self.frmC, text='保存批量检测结果', width = 15, command=save_result)
        
        # 表格布局
        self.ButtonC1.grid(row=0, column=0,padx=2, pady=2)
        self.ButtonC2.grid(row=0, column=1,padx=2, pady=2)
        self.ButtonC3.grid(row=0, column=2,padx=2, pady=2)
        self.ButtonC4.grid(row=0, column=3,padx=2, pady=2)
        self.ButtonC5.grid(row=0, column=4,padx=2, pady=2)
        self.ButtonC6.grid(row=0, column=5,padx=2, pady=2)

    #创造第四象限
    def CreateFourth(self):
        self.ButtonE1 = Button(self.frmE, text='加载POC', width = 8, command=self.LoadPoc)
        self.ButtonE2 = Button(self.frmE, text='编辑文件', width = 8, command=lambda:thread_it(CodeFile, **{
            'root':gui.root,
            'file_name':MyGUI.Checkbutton_text,
            'Logo':'1',
            'vuln_select':MyGUI.vuln,
            'text':'',
            }))
        self.ButtonE3 = Button(self.frmE, text='打开脚本目录', width = 10, command=lambda:LoadCMD('/POC'))
        self.ButtonE1.grid(row=0, column=0, padx=2, pady=2)
        self.ButtonE2.grid(row=0, column=1, padx=2, pady=2)
        self.ButtonE3.grid(row=0, column=2, padx=2, pady=2)

    def CreateFivth(self):
        # 创建Notebook组件
        self.note1 = ttk.Notebook(self.frmD, width=300,height=580, style='my.TNotebook')
        self.ButtonF1 = Button(self.frmF, text='<-', width = 15, command=lambda:self.switch_frm('<-'))
        self.ButtonF2 = Button(self.frmF, text='->', width = 15, command=lambda:self.switch_frm('->'))
        self.ButtonF1.pack(side=LEFT, expand=1, fill=BOTH)
        self.ButtonF2.pack(side=RIGHT, expand=1, fill=BOTH)

    # 切换界面
    def switch_frm(self, str):
        ilist = []
        jdcit = {}
        index = self.note1.index('current')
        text = self.note1.tab(index)['text']
        tabs_list = self.note1.tabs()
        for i in tabs_list:
            if self.note1.tab(i)['text'] == text:
                # 下标
                ilist.append(self.note1.index(i))
                # self.note1.index(i)
                jdcit.update({self.note1.index(i):i})
        # 定位
        pos = ilist.index(index)
        if str == '<-':
            if pos == 0:
                return
            else:
                # 隐藏当前界面
                self.note1.hide(self.note1.index('current'))
                # 显示界面
                self.note1.add(jdcit[ilist[pos-1]])
                # 选择指定的选项卡
                self.note1.select(jdcit[ilist[pos-1]])
        elif str == '->':
            if pos == len(ilist) - 1:
                return
            else:
                # 隐藏当前界面
                self.note1.hide(self.note1.index('current'))
                # 显示界面
                self.note1.add(jdcit[ilist[pos+1]])
                # 选择指定的选项卡
                self.note1.select(jdcit[ilist[pos+1]])
                
    # 加载POC
    def LoadPoc(self):
        # 清空存储
        self.note1.destroy()
        MyGUI.uppers.clear()
        MyGUI.scripts.clear()
        MyGUI.var.clear()
        for frm in MyGUI.frms:
            self.frms[frm] = None
        MyGUI.frms.clear()
        style1 = ttk.Style()
        # 'se'再改nw,ne,sw,se,w,e,wn,ws,en,es,n,s试试
        style1.configure('my.TNotebook', tabposition='wn')
        # 创建Notebook组件
        self.note1 = ttk.Notebook(self.frmD, width=300,height=580, style='my.TNotebook')
        self.note1.pack(expand=1, fill=BOTH)
        try:
            for _ in glob.glob('POC/*.py'):
                script_name = os.path.basename(_).replace('.py', '')
                if script_name in ['__init__','GlobSettings']:
                    continue
                i = script_name[0].upper()
                if i not in MyGUI.uppers:
                    MyGUI.uppers.append(i)
                MyGUI.scripts.append(script_name)
                m = IntVar()
                MyGUI.var.update({script_name:m})
            # 去重
            MyGUI.uppers = list(set(MyGUI.uppers))
            # 排序
            MyGUI.uppers.sort()
            self.CreateThread()
        except Exception as e:
            messagebox.showinfo('提示','请勿重复加载')
            
    # 填充线程列表,创建多个存储POC脚本的界面
    def CreateThread(self):
        for i in MyGUI.uppers:
            index = 1
            for script_name in MyGUI.scripts:
                if script_name.upper().startswith(i):
                    if self.frms.get('frmD_'+i+'_'+str(math.ceil(index/18)), None) is None:
                        MyGUI.frms.append('frmD_'+i+'_'+str(math.ceil(index/18)))
                        # self.frmD width=300, height=580
                        self.frms['frmD_'+i+'_'+str(math.ceil(index/18))] = Frame(self.frmD, width=290, height=580, bg='whitesmoke')
                        # 装入框架到选项卡
                        self.note1.add(self.frms['frmD_'+i+'_'+str(math.ceil(index/18))], text=i)
                    self.Create(self.frms['frmD_'+i+'_'+str(math.ceil(index/18))],script_name,index)
                    index += 1
            # 只显示一个界面
            if index > 18:
                # 装入框架到选项卡
                self.note1.hide(self.frms['frmD_'+i+'_'+str(math.ceil(index/18))])

    # 创建POC脚本选择Checkbutton
    def Create(self, frm, x, i):
        button = Checkbutton(frm,text=x, variable=MyGUI.var[x], command=lambda:self.callCheckbutton(x))
        button.grid(row=i, sticky=W)

    # 调用checkbutton按钮
    def callCheckbutton(self, x):
        if MyGUI.var[x].get() == 1:
            try:
                for key, value in MyGUI.var.items():
                    if key != x:
                        value.set(0)
                MyGUI.vuln = importlib.import_module('.%s'%x,package='POC')
                MyGUI.Checkbutton_text = x
                print('[*] %s 模块已准备就绪!'%x)
            except Exception as e:
                print('[*]异常对象的内容是:%s'%e)
        else:
            MyGUI.vuln = None
            print('[*] %s 模块已取消!'%x)

    # 多线程函数
    def thread_it(self, func, **kwargs):
        self.t = threading.Thread(target=func,kwargs=kwargs)
        # 守护
        self.t.setDaemon(True)
        # 启动
        self.t.start()

    # 停止线程
    def stop_thread(self):
        try:
            _async_raise(self.t.ident, SystemExit)
            print("[*]已停止运行")
        except Exception as e:
            messagebox.showinfo('错误',str(e))
        finally:
            gui.TexA2.delete('1.0','end')
            gui.TexA2.configure(state="disabled")

    # 验证功能
    def BugTest(self,**kwargs):
        # 未选中模块
        if MyGUI.vuln == None:
            messagebox.showinfo(title='提示', message='还未选择模块')
            return
        MyGUI.vul_name = MyGUI.vuln.__name__.replace('POC.', '')
        # 进度条初始化
        self.frame_progress.pBar["value"] = 0
        self.root.update()
        # 是否需要保存结果
        MyGUI.wbswitch = 'false'
        start = time.time()
        color('[*]开始执行模块 %s'%MyGUI.vul_name,'blue')
        # 进入单模块测试功能
        if kwargs['url']:
            try:
                # 运行状态子线程
                self.t2 = threading.Thread(target=wait_running, name='运行状态子线程', daemon=True)
                self.t2.start()
                MyGUI.vuln.check(**kwargs)
            except Exception as e:
                print('出现错误: %s'%e)
            finally:
                _async_raise(self.t2.ident, SystemExit)
                gui.TexA2.delete('1.0','end')
                gui.TexA2.configure(state="disabled")
            end = time.time()
            print('[*]共花费时间：{} 秒'.format(seconds2hms(end - start)))
        # 进入多目标测试功能
        elif myurls.TexA.get('0.0', 'end').strip('\n'):
            # 去空处理
            file_list = [i for i in myurls.TexA.get('0.0','end').split("\n") if i!='']
            file_len = len(file_list)
            # 每执行一个任务增长的长度
            flag = round(1000/file_len, 2)
            executor = ThreadPoolExecutor(max_workers = int(kwargs['pool']))
            # 存储目标列表
            url_list = []
            # 存储结果列表
            result_list = []
            for url in file_list:
                args = {'url':url}
                url_list.append(args)
            try:
                for data in executor.map(lambda kwargs: MyGUI.vuln.check(**kwargs), url_list):
                    # 如果结果是列表,去重一次
                    if type(data) == list:
                        data = list(set(data))
                    # 汇聚结果
                    result_list.append(data)
                    # 进度条
                    self.frame_progress.pBar["value"] += flag
                    self.root.update()
                # 根据结果生成表格
                index_list = [i+1 for i in range(len(url_list))]
                # 合并列表
                print_result = zip(index_list, file_list, result_list)
                tb = pt.PrettyTable()
                tb.field_names = ["Index", "URL", "Result"]
                tb.align['URL'] = 'l'
                tb.align['Result'] = 'l'
                # 保存结果
                MyGUI.wbswitch = 'true'
                # 构造初始环境
                # 当前结果文件
                MyGUI.wb = Workbook()
                # excel表格
                MyGUI.ws = MyGUI.wb.active
                MyGUI.ws.append(['Index','URL', 'Result'])
                index = 1
                # 输出结果
                for i in print_result:
                    MyGUI.ws.append(i)
                    tb.add_row(i)
                    index += 1
                print(tb)
                # 关闭线程池
                executor.shutdown()
            except Exception as e:
                print('执行脚本出现错误: %s ,建议在脚本加上异常处理!'%type(e))
                self.frame_progress.pBar["value"] = 1000
                self.root.update()
            finally:
                end = time.time()
                print('[*]共花费时间：{} 秒'.format(seconds2hms(end - start)))
        # 没有输入测试目标
        else:
            color('[*]请输入目标URL!','red')
            color('[*]请输入目标URL!','yellow')
            color('[*]请输入目标URL!','blue')
            color('[*]请输入目标URL!','green')
            color('[*]请输入目标URL!','orange')
            color('[*]请输入目标URL!','pink')
            color('[*]请输入目标URL!','cyan')

    # 开始循环
    def start(self):
        self.CreateFrm()
        self.CreateFirst()
        self.CreateSecond()
        self.CreateThird()
        self.CreateFourth()
        self.CreateFivth()
        
class Ysoserial_ter():
    ysotype_list = ['-jar','-cp']
    ysoclass_list = ['BeanShell1','C3P0','Clojure','CommonsBeanutils1','CommonsCollections1','CommonsCollections2',
        'CommonsCollections3','CommonsCollections4','CommonsCollections5','CommonsCollections6','CommonsCollections7',
        'CommonsCollections8','CommonsCollections9','CommonsCollections10','FileUpload1','Groovy1','Hibernate1','Hibernate2',
        'JBossInterceptors1','JRMPClient','JRMPListener','JSON1','JavassistWeld1','Jdk7u21','Jython1','MozillaRhino1','MozillaRhino2',
        'Myfaces1','Myfaces2','ROME','ShiroCheck','Spring1','Spring2','Spring3','URLDNS','Vaadin1','Wicket1']

    ysoother_list = ['ysoserial.my.DirectiveProcessor','ysoserial.Deserializer']
    java_payload = None
    def __init__(self,root):
        self.yso = Toplevel(root)
        self.yso.title("ysoserial代码生成")
        self.yso.geometry('950x600+650+150')
        # self.exchange = self.yso.resizable(width=False, height=False)#不允许扩大

        
        self.frmA = Frame(self.yso, width=945, height=90,bg="white")
        self.frmB = Frame(self.yso, width=945, height=500,bg="white")
        self.frmA.grid(row=0, column=0, padx=2, pady=2)
        self.frmB.grid(row=1, column=0, padx=2, pady=2)
        #self.frmB.place(relx = 0, rely = 0)
        self.frmA.grid_propagate(0)
        self.frmB.grid_propagate(0)

        #参数配置,上半区
        self.frame_1 = LabelFrame(self.frmA, text="参数配置", labelanchor="nw", width=940, height=85, bg='whitesmoke')
        self.frame_1.grid(row=0, column=0, padx=2, pady=2)
        self.frame_1.grid_propagate(0)

        self.frame_1_A = Frame(self.frame_1, width=930, height=30,bg="whitesmoke")
        self.frame_1_B = Frame(self.frame_1, width=930, height=30,bg="whitesmoke")

        self.frame_1_A.grid(row=0, column=0, padx=1, pady=1)
        self.frame_1_B.grid(row=1, column=0, padx=1, pady=1)

        self.frame_1_A.grid_propagate(0)
        self.frame_1_B.grid_propagate(0)

        #第一行
        self.label_1 = Label(self.frame_1_A, text="ysoserial:")
        self.comboxlist_A_type = ttk.Combobox(self.frame_1_A,width='10',textvariable=Ent_yso_Top_type,state='readonly',font=("consolas",10))
        self.comboxlist_A_type["values"] = tuple(Ysoserial_ter.ysotype_list)
        self.comboxlist_A_type.bind("<<ComboboxSelected>>", self.change_type)

        self.comboxlist_A_class = ttk.Combobox(self.frame_1_A,width='35',textvariable=Ent_yso_Top_class,state='readonly',font=("consolas",10))
        self.comboxlist_A_class["values"] = tuple(Ysoserial_ter.ysoclass_list)
        self.comboxlist_A_class.bind("<<ComboboxSelected>>", self.change_class)

        self.label_1.grid(row=0,column=0,padx=2, pady=2, sticky=W)
        self.comboxlist_A_type.grid(row=0,column=1,padx=2, pady=2, sticky=W)
        self.comboxlist_A_class.grid(row=0,column=2,padx=2, pady=2, sticky=W)

        #第二行
        self.label_2 = Label(self.frame_1_B, text="inputcmds:")
        self.EntA_2 = Entry(self.frame_1_B, width='110', highlightcolor='red', highlightthickness=1,textvariable=Ent_yso_Top_cmd,font=("consolas",10))
        self.button_2 = Button(self.frame_1_B, text="Exploit", width=10, command=self.Exploit)

        self.label_2.grid(row=0,column=0,padx=2, pady=2,sticky=W)
        self.EntA_2.grid(row=0,column=1,padx=2, pady=2,sticky=W)
        self.button_2.grid(row=0,column=2,padx=2, pady=2,sticky=W)


        #下半区
        self.TexB_A = scrolledtext.ScrolledText(self.frmB,font=("consolas",10),width=132, height=16)
        self.separ = ttk.Separator(self.frmB, orient=HORIZONTAL, style='red.TSeparator')
        self.TexB_B = scrolledtext.ScrolledText(self.frmB,font=("consolas",10),width=132, height=16)

        self.TexB_A.grid(row=0,column=0,padx=2, pady=2,sticky=W)
        self.separ.grid(row=1, column=0, sticky='ew')
        self.TexB_B.grid(row=2,column=0,padx=2, pady=2,sticky=W)

        self.TexB_A.bind("<Button-3>", lambda x: self.rightKey(x, gui.menubar_1))#绑定右键鼠标事件

    def change_type(self,*args):
        java_type = Ent_yso_Top_type.get()
        if java_type == '-cp':
            self.comboxlist_A_class["values"] = tuple(Ysoserial_ter.ysoother_list)
        else:
            self.comboxlist_A_class["values"] = tuple(Ysoserial_ter.ysoclass_list)
        self.comboxlist_A_class.current(0)

    def change_class(self,*args):
        java_class = Ent_yso_Top_class.get()
        if java_class == 'ysoserial.Deserializer':
            Ent_yso_Top_cmd.set('提示: 请输入序列化后的文件名')
        else:
            Ent_yso_Top_cmd.set('whoami')
        
    def Exploit(self):
        java_type = Ent_yso_Top_type.get()
        java_class = Ent_yso_Top_class.get()
        java_cmd = Ent_yso_Top_cmd.get().strip('\n')
        
        try:
            Ysoserial_ter.java_payload = ysoserial_payload(java_type=java_type,java_class=java_class,java_cmd=java_cmd)
            self.TexB_A.delete('1.0','end')
            self.TexB_A.insert(INSERT, binascii.hexlify(Ysoserial_ter.java_payload).decode())
            #self.TexB_A.configure(state="disabled")
        except Exception as e:
            Ysoserial_ter.java_payload = None
            messagebox.showinfo(title='错误!', message=str(e))

    def rightKey(self, event, menubar):
        menubar.delete(0,END)
        #menubar.add_command(label='a2b_hex',command=lambda:self.a2b_hex(self.TexB_A.get(1.0, "end").strip('\n')))
        menubar.add_command(label='b2a_base64',command=lambda:self.b2a_base64(self.TexB_A.get(1.0, "end").strip('\n')))
        menubar.add_command(label='save_file',command=self.save_file)
        #menubar.add_command(label='a2b_save_file',command=self.save_file)
        menubar.post(event.x_root,event.y_root)


    def a2b_hex(self, now_text):
        try:
            text = binascii.a2b_hex(now_text).decode()
            self.TexB_B.delete('1.0','end')
            self.TexB_B.insert(INSERT, text)
        except Exception as e:
            messagebox.showinfo(title='错误!', message=str(e))

    def b2a_base64(self, now_text):
        try:
            text = base64.b64encode(binascii.a2b_hex(now_text)).decode()  #加密
            self.TexB_B.delete('1.0','end')
            self.TexB_B.insert(INSERT, text)
        except Exception as e:
            messagebox.showinfo(title='错误!', message=str(e))

    def save_file(self):
        file_path = filedialog.asksaveasfilename(title=u'保存文件')
        if file_path:
            try:
                with open(file=file_path, mode='wb+') as file:
                    file.write(Ysoserial_ter.java_payload)
                messagebox.showinfo(title='提示', message='保存成功')
            except Exception as e:
                messagebox.showinfo(title='错误!', message=str(e))


class Data_debug():
    def __init__(self, root):
        self.Debug = Toplevel(root)
        self.Debug.title("TCP调试工具")
        self.Debug.geometry('700x450+650+150')
        self.Debug.protocol("WM_DELETE_WINDOW", self.callbackClose)
        self.exchange = self.Debug.resizable(width=False, height=False)#不允许扩大

        self.frmLeft = Frame(self.Debug, width=345, height=450, bg="whitesmoke")
        self.frmRight = Frame(self.Debug, width=345, height=450, bg="whitesmoke")
        self.frmLeft.grid(row=0, column=0, padx=2, pady=2)
        self.frmRight.grid(row=0, column=1, padx=2, pady=2)

        self.frmLeft.grid_propagate(0)
        self.frmRight.grid_propagate(0)
        
        self.LA = Frame(self.frmLeft, width=340, height=50, bg="whitesmoke")
        self.LB = Frame(self.frmLeft, width=340, height=300, bg="whitesmoke")
        self.LC = Frame(self.frmLeft, width=340, height=100, bg="whitesmoke")
        
        self.LA.grid_propagate(0)
        self.LB.grid_propagate(0)
        self.LC.grid_propagate(0)
        self.LA.grid(row=0, column=0, padx=2, pady=2)
        self.LB.grid(row=1, column=0, padx=2, pady=2)
        self.LC.grid(row=2, column=0, padx=2, pady=2)
        
        """
        :目的IP
        :端  口
        """
        self.LA_LabA = Label(self.LA, text='目的IP')#目的IP
        self.LA_EntA = Entry(self.LA, width='20',highlightcolor='red', highlightthickness=1,textvariable=TCP_Debug_IP,font=("consolas",10))#IP
        self.LA_LabB = Label(self.LA, text='端   口')#目的端口
        self.LA_EntB = Entry(self.LA, width='10',highlightcolor='red', highlightthickness=1,textvariable=TCP_Debug_PORT,font=("consolas",10))#PORT
        
        self.LA_LabA.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.LA_EntA.grid(row=0, column=1, padx=2, pady=2, sticky=W)
        self.LA_LabB.grid(row=1, column=0, padx=2, pady=2, sticky=W)
        self.LA_EntB.grid(row=1, column=1, padx=2, pady=2, sticky=W)
        """
        """
        self.LB_top = Frame(self.LB, width=340, height=30, bg="whitesmoke")
        self.LB_bottom = Frame(self.LB, width=340, height=270, bg="whitesmoke")
        self.LB_top.grid_propagate(0)
        self.LB_bottom.grid_propagate(0)
        self.LB_top.grid(row=0, column=0, padx=2, pady=2)
        self.LB_bottom.grid(row=1, column=0, padx=2, pady=2)
        
        #self.LB_top_checkbutton_1 = Button(self.LB_top, text='connect', width=9, activebackground = "whitesmoke", command=lambda :thread_it(self.connect))
        self.LB_top_checkbutton_2 = Button(self.LB_top, text='send', width=9, activebackground = "whitesmoke", command=lambda : thread_it(self.send))
        self.LB_top_checkbutton_3 = Button(self.LB_top, text='close', width=9, activebackground = "whitesmoke", command=lambda : thread_it(self.close))
        
        #self.LB_top_checkbutton_1.grid(row=0, column=0, padx=2, pady=2)
        self.LB_top_checkbutton_2.grid(row=0, column=0, padx=2, pady=2)
        self.LB_top_checkbutton_3.grid(row=0, column=1, padx=2, pady=2)
        """
        """
        self.LB_bottom_TexA = scrolledtext.ScrolledText(self.LB_bottom,font=("consolas",10),width='45',height='17', undo = True)
        self.LB_bottom_TexA.grid(row=0, column=0, padx=2, pady=2)
        """
        """
        self.LC_TexC = scrolledtext.ScrolledText(self.LC,font=("consolas",10),width='45',height='5', undo = True)
        self.LC_TexC.grid(row=0, column=0, padx=2, pady=2)
        """
        """
        self.LD = Frame(self.frmRight, width=340, height=30, bg="whitesmoke")
        self.LE = Frame(self.frmRight, width=340, height=410, bg="whitesmoke")
        
        self.LD.grid_propagate(0)
        self.LE.grid_propagate(0)
        self.LD.grid(row=0, column=0, padx=2, pady=2)
        self.LE.grid(row=1, column=0, padx=2, pady=2)
        
        self.LD_LabA = Label(self.LD, text="接收缓冲区大小")
        self.LD_LabB = Label(self.LD, text="字节")
        self.LD_EntA = Entry(self.LD, width='10',highlightcolor='red', highlightthickness=1,textvariable=TCP_Debug_PKT_BUFF_SIZE,font=("consolas",10))#URL
        self.LD_LabA.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.LD_LabB.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.LD_EntA.grid(row=0, column=1, padx=2, pady=2, sticky=W)
        
        self.frmRight_TexC = scrolledtext.ScrolledText(self.LE,font=("consolas",10),width='45',height='27', undo = True)
        self.frmRight_TexC.bind("<Button-3>", lambda x: self.rightKey(x, gui.menubar_1))#绑定右键鼠标事件
        self.frmRight_TexC.grid(row=0, column=0, padx=2, pady=2)
        
        """
        输出重定向
        """
        #sys.stdout = TextRedirector(self.LC_TexC, "stdout")
        #sys.stderr = TextRedirector(self.LC_TexC, "stderr")
        
    def connect(self):
        remote_ip = TCP_Debug_IP.get()
        remote_port = TCP_Debug_PORT.get()
        
        self.remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.remote_conn.setblocking(True)
        try:
            self.remote_conn.settimeout(3)
            self.remote_conn.connect((remote_ip, remote_port))
            print("["+str(datetime.datetime.now())[11:19]+"] " + '[+] Establish connection success to %s %s'%(remote_ip, remote_port))
            self.recv_thread = threading.Thread(target=self.recv,daemon=True)
            self.recv_thread.start()
        except Exception as e:
            self.remote_conn.close()
            self.remote_conn = None
            print("["+str(datetime.datetime.now())[11:19]+"] " + '[-] Establish connection failed %s'%e)
        
    def close(self):
        try:
            _async_raise(self.recv_thread.ident, SystemExit)
            self.remote_conn.close()
            print("["+str(datetime.datetime.now())[11:19]+"] " + '[+] Closed socket success')
        except Exception as e:
            print("["+str(datetime.datetime.now())[11:19]+"] " + '[-] Failed Closing socket. %s'%e)

    def send(self):
        self.connect()
        if self.remote_conn:
            try:
                data_raw = self.LB_bottom_TexA.get('0.0','end').strip('\n')
                #output = binascii.unhexlify(data_raw)
                #data_send = output.decode("utf-8", "ignore")
                data_send = bytes.fromhex(data_raw)
                self.remote_conn.sendall(data_send)
                print("["+str(datetime.datetime.now())[11:19]+"] " + '[+] Send data %s bytes'%len(data_send))
            except Exception as e:
                print("["+str(datetime.datetime.now())[11:19]+"] " + '[-] Failed sending data. %s'%e)

    def recv(self):
        self.frmRight_TexC.delete('1.0','end')
        while True:
            try:
                #print(TCP_Debug_PKT_BUFF_SIZE.get())
                data_recv_raw = self.remote_conn.recv(TCP_Debug_PKT_BUFF_SIZE.get())
                if data_recv_raw:
                    print("["+str(datetime.datetime.now())[11:19]+"] " + '[+] Received data %s bytes'%len(data_recv_raw))
                    #print('[-] No more data is received.')
                    break
            except Exception as e:
                print("["+str(datetime.datetime.now())[11:19]+"] " + '[-] Failed recving data. %s'%e)
        data_recv = binascii.hexlify(data_recv_raw)
        self.frmRight_TexC.insert(INSERT, data_recv)
        self.close()
        return

    def rightKey(self, event, menubar):
        menubar.delete(0,END)
        #menubar.add_command(label='a2b_hex',command=lambda:self.a2b_hex(self.TexB_A.get(1.0, "end").strip('\n')))
        menubar.add_command(label='hex_to_str',command=lambda:self.hex_to_str(self.frmRight_TexC.get(1.0, "end").strip('\n')))
        #menubar.add_command(label='save_file',command=self.save_file)
        #menubar.add_command(label='a2b_save_file',command=self.save_file)
        menubar.post(event.x_root,event.y_root)

    def hex_to_str(self, hex_byte):
        try:
            a_byte = binascii.unhexlify(hex_byte) #unhexlify()传入的参数也可以是b'xxxx'(xxxx要符合16进制特征)
            text = a_byte.decode("utf-8", "ignore")
            self.frmRight_TexC.delete('1.0','end')
            self.frmRight_TexC.insert(INSERT, text)
        except Exception as e:
            messagebox.showinfo(title='错误!', message=str(e))

    #退出函数
    def callbackClose(self):
        #sys.stdout = TextRedirector(gui.TexB, "stdout")
        #sys.stderr = TextRedirector(gui.TexB, "stderr")
        #self.close()
        self.Debug.destroy()

# 漏洞利用界面类
class MyEXP:
    def __init__(self, gui):
        self.frmEXP = gui.frmEXP
        self.root = gui.root
        # 创建一个菜单
        self.menubar = Menu(self.root, tearoff=False)

    def CreateFrm(self):
        self.frmTOP = Frame(self.frmEXP, width=1160, height=130, bg='whitesmoke')
        self.frmBOT = Frame(self.frmEXP, width=1160, height=570, bg='whitesmoke')
        # expand=0, fill=X 只允许X轴反向扩张
        self.frmTOP.pack(side=TOP, expand=0, fill=X)
        # expand=1, fill=BOTH 全方位扩张
        self.frmBOT.pack(side=BOTTOM, expand=1, fill=BOTH)
        # 目标，输入框
        self.frmA = Frame(self.frmTOP, width=670, height=120,bg='whitesmoke')
        # 输出信息
        self.frmB = Frame(self.frmTOP, width=490, height=120, bg='whitesmoke')
        # # grid布局
        # self.frmA.grid(row=0, column=0, padx=1, pady=1)
        # self.frmB.grid(row=0, column=1, padx=1, pady=1)
        # pack布局
        self.frmA.pack(side=LEFT, expand=1, fill=BOTH)
        self.frmB.pack(side=RIGHT, expand=1, fill=BOTH)

    def CreateFirst(self):
        self.frame_1 = LabelFrame(self.frmA, text="基本配置", labelanchor="nw", width=660, height=130, bg='whitesmoke')
        # pack布局
        self.frame_1.pack(expand=1, fill=BOTH)
        # 基本配置
        self.frame_1_1 = Frame(self.frame_1, width=660, height=40, bg='whitesmoke')
        self.frame_1_2 = Frame(self.frame_1, width=660, height=40, bg='whitesmoke')
        self.frame_1_3 = Frame(self.frame_1, width=660, height=40, bg='whitesmoke')
        # pack布局
        self.frame_1_1.pack(side=TOP, expand=0, fill=X)
        self.frame_1_2.pack(side=TOP, expand=0, fill=X)
        self.frame_1_3.pack(side=TOP, expand=0, fill=X)
        
        self.label_1_1 = Label(self.frame_1_1, text="目标地址")
        self.EntA_1_1 = Entry(self.frame_1_1, width='55',highlightcolor='red', highlightthickness=1,textvariable=Ent_B_Top_url, font=("consolas",10))
        self.Button_1_1 = Button(self.frame_1_1, text='......', width=6, command=lambda :myurls.show())
        
        self.label_1_1.pack(side=LEFT, expand=0, fill=NONE)
        self.EntA_1_1.pack(side=LEFT, expand=1, fill=X)
        self.Button_1_1.pack(side=LEFT, expand=0, fill=NONE)
        
        self.label_1_2 = Label(self.frame_1_2, text="认证头部")
        self.EntA_1_2 = Entry(self.frame_1_2, width='55',highlightcolor='red', highlightthickness=1,textvariable=Ent_B_Top_cookie,font=("consolas",10))
        self.label_1_2.pack(side=LEFT, expand=0, fill=NONE)
        self.EntA_1_2.pack(side=LEFT, expand=1, fill=X)
        
        self.label_1_3 = Label(self.frame_1_3, text="漏洞名称")
        self.comboxlist_1_3 = ttk.Combobox(self.frame_1_3,width='17',textvariable=Ent_B_Top_vulname,state='readonly')
        self.comboxlist_1_3["values"] = tuple(exp_scripts)
        self.comboxlist_1_3.bind("<<ComboboxSelected>>", bind_combobox)
        self.comboxlist_1_3_1 = ttk.Combobox(self.frame_1_3,width='32',textvariable=Ent_B_Top_vulmethod,state='readonly')
        self.button_1_3 = Button(self.frame_1_3, text="编辑文件", width=6, command=lambda:thread_it(CodeFile,**{
            'root':gui.root,
            'file_name':Ent_B_Top_vulname.get(),
            'Logo':'2',
            'vuln_select':myexp_vuln,
            'text':Ent_B_Top_vulmethod.get(),
            }))
        self.label_1_3.pack(side=LEFT, expand=0, fill=NONE)
        self.comboxlist_1_3.pack(side=LEFT, expand=1, fill=X)
        self.comboxlist_1_3_1.pack(side=LEFT, expand=1, fill=X)
        self.button_1_3.pack(side=LEFT, expand=0, fill=NONE)

    def CreateSecond(self):
        self.frame_B1 = LabelFrame(self.frmB, text="参数配置", labelanchor="nw", width=400, height=130, bg='whitesmoke')
        # pack布局
        self.frame_B1.pack(expand=1, fill=BOTH)

        self.label_4 = Label(self.frame_B1, text="命令执行(True/False)")
        self.comboxlist_4 = ttk.Combobox(self.frame_B1,width='6',textvariable=Ent_B_Top_funtype,state='readonly') #接受输入控件
        self.comboxlist_4["values"] = tuple(['True','False'])
        self.comboxlist_4.bind("<<ComboboxSelected>>", bind_combobox_3)

        self.label_5 = Label(self.frame_B1, text="超时时间(Timeout)")
        self.b5 = Spinbox(self.frame_B1,from_=1,to=10,wrap=True,width=3,font=("consolas",10),textvariable=Ent_B_Top_timeout)

        self.label_6 = Label(self.frame_B1, text="请求次数(retry_time)")
        self.b6 = Spinbox(self.frame_B1,from_=1,to=10,wrap=True,width=3,font=("consolas",10),textvariable=Ent_B_Top_retry_time)

        self.label_7 = Label(self.frame_B1, text="重试间隔(retry_interval)")
        self.b7 = Spinbox(self.frame_B1,from_=1,to=10,wrap=True,width=3,font=("consolas",10),textvariable=Ent_B_Top_retry_interval)
        
        self.label_8 = Label(self.frame_B1, text="线程数量(pool_num)")
        self.b8 = Spinbox(self.frame_B1,from_=1,to=30,wrap=True,width=3,font=("consolas",10),textvariable=Ent_B_Top_thread_pool)

        self.label_4.grid(row=2,column=0,padx=2, pady=2, sticky=W)
        self.comboxlist_4.grid(row=2,column=1,padx=2, pady=2, sticky=W)

        self.label_5.grid(row=0,column=2,padx=2, pady=2, sticky=W)
        self.b5.grid(row=0,column=3,padx=2, pady=2, sticky=W)

        self.label_6.grid(row=1,column=0,padx=2, pady=2, sticky=W)
        self.b6.grid(row=1,column=1,padx=2, pady=2, sticky=W)      

        self.label_7.grid(row=1,column=2,padx=2, pady=2, sticky=W)
        self.b7.grid(row=1,column=3,padx=2, pady=2, sticky=W)
    
        self.label_8.grid(row=0,column=0,padx=2, pady=2, sticky=W)
        self.b8.grid(row=0,column=1,padx=2, pady=2, sticky=W)

    def CreateThird(self):
        self.frmBOT_1 = LabelFrame(self.frmBOT, text="命令执行", labelanchor="nw", width=1160, height=570, bg='whitesmoke')
        self.frmBOT_1_1 = Frame(self.frmBOT_1, width=1160, height=20, bg='whitesmoke')
        self.frmBOT_1_2 = Frame(self.frmBOT_1, width=1160, height=550, bg='whitesmoke')
        self.frmBOT_1_3 = Frame(self.frmBOT_1, width=1160, height=10, bg='whitesmoke')

        self.frmBOT_1.pack(expand=1, fill=BOTH)
        self.frmBOT_1_1.pack(side=TOP, expand=0, fill=X)
        self.frmBOT_1_2.pack(side=TOP, expand=1, fill=BOTH)
        self.frmBOT_1_3.pack(side=TOP, expand=0, fill=X)

        self.labelBOT_1 = Label(self.frmBOT_1_1, text="CMD命令")
        self.EntABOT_1 = Entry(self.frmBOT_1_1, width='91',highlightcolor='red', highlightthickness=1,textvariable=Ent_B_Bottom_Left_cmd,font=("consolas",10)) #接受输入控件
        self.EntABOT_1.insert(0, "echo " + GlobalVar.get_value('flag'))
        self.buttonBOT_1 = Button(self.frmBOT_1_1, text="执行任务",command=lambda : thread_it(exeCMD,**{
            'url' : Ent_B_Top_url.get().strip('/'),
            'cookie' : Ent_B_Top_cookie.get(),
            'cmd' : Ent_B_Bottom_Left_cmd.get(),
            'pocname' : Ent_B_Top_vulmethod.get(),
            'vuln' : Ent_B_Top_funtype.get(),
            'timeout' : int(Ent_B_Top_timeout.get()),
            'retry_time' : int(Ent_B_Top_retry_time.get()),
            'retry_interval' : int(Ent_B_Top_retry_interval.get()),
            'pool_num' : int(Ent_B_Top_thread_pool.get()),
            }
        ))
        # 功能按钮
        self.buttonBOT_2 = Button(self.frmBOT_1_1, text='取消任务', command=lambda : thread_it(CancelThread()))
        self.buttonBOT_3 = Button(self.frmBOT_1_1, text='清空信息', command=lambda : delText(exp.TexBOT_1_2))
        # pack布局
        self.labelBOT_1.pack(side=LEFT, expand=0, fill=NONE)
        self.EntABOT_1.pack(side=LEFT, expand=1, fill=X)
        self.buttonBOT_1.pack(side=LEFT, expand=0, fill=NONE)
        self.buttonBOT_2.pack(side=LEFT, expand=0, fill=NONE)
        self.buttonBOT_3.pack(side=LEFT, expand=0, fill=NONE)
        # 文本框
        self.TexBOT_1_2 = scrolledtext.ScrolledText(self.frmBOT_1_2, font=("consolas",9), width=138, height=26, bg='black')
        # 绑定右键鼠标事件
        self.TexBOT_1_2.bind("<Button-3>", lambda x: self.rightKey(x, self.menubar))
        # 提前定义颜色
        self.TexBOT_1_2.tag_add("here", "1.0","end")
        self.TexBOT_1_2.tag_config("here", background="black")
        self.TexBOT_1_2.pack(expand=1, fill=BOTH)
        # 进度条
        self.frame_progress = FrameProgress(self.frmBOT_1_3, height=10, maximum=1000)
        self.frame_progress.pack(side=BOTTOM, expand=0, fill=X)

    def rightKey(self, event, menubar):
        menubar.delete(0,END)
        menubar.add_command(label='在浏览器显示结果', command=lambda:open_html('./EXP/output.html'))
        #menubar.add_command(label='打开命令执行终端',command=lambda:Terminal_Infos(gui.root))
        menubar.add_command(label='刷新EXP脚本', command=RefreshEXP)
        menubar.post(event.x_root,event.y_root)

    def start(self):
        self.CreateFrm()
        self.CreateFirst()
        self.CreateSecond()
        self.CreateThird()

# 漏洞测试界面类
class Mycheck:
    # 请求类型
    Get_type = ['GET','POST','PUT','DELETE']
    def __init__(self, gui):
        self.frmCheck = gui.frmCheck
        self.root = gui.root
        self.columns = ("字段", "值")
        self.Type = ['User-Agent','Connection','Accept-Encoding','Accept']
        self.Value = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0','close','gzip, deflate','*/*']

    def CreateFrm(self):
        self.frmleft = Frame(self.frmCheck, width=520, height=700,bg='whitesmoke')
        self.frmright = Frame(self.frmCheck, width=640, height=700,bg='whitesmoke')
        # 布局
        self.frmleft.pack(side=LEFT, expand=1, fill=BOTH)
        self.frmright.pack(side=RIGHT, expand=1, fill=BOTH)

        self.frmleft_1 = Frame(self.frmleft, width=520, height=90,bg='whitesmoke')
        self.frmleft_2 = Frame(self.frmleft, width=520, height=260,bg='whitesmoke')
        self.frmleft_3 = Frame(self.frmleft, width=520, height=350,bg='whitesmoke')
        self.frmleft_1.pack(side=TOP, expand=0, fill=X)
        self.frmleft_2.pack(side=TOP, expand=0, fill=X)
        self.frmleft_3.pack(side=TOP, expand=1, fill=BOTH)

    def CreateFirst(self):
        pass

    def CreateSecond(self):
        self.frmleft_1_1 = Frame(self.frmleft_1, width=520, height=30, bg='whitesmoke')
        self.frmleft_1_2 = Frame(self.frmleft_1, width=520, height=30, bg='whitesmoke')
        self.frmleft_1_3 = Frame(self.frmleft_1, width=520, height=30, bg='whitesmoke')
        self.frmleft_1_1.pack(side=TOP, expand=1, fill=BOTH)
        self.frmleft_1_2.pack(side=TOP, expand=1, fill=BOTH)
        self.frmleft_1_3.pack(side=TOP, expand=1, fill=BOTH)
        
        self.label_1 = Label(self.frmleft_1_1, text="请求方法")
        # 请求方法类型
        self.comboxlist_1 = ttk.Combobox(self.frmleft_1_1,width='15',textvariable=Ent_C_Top_reqmethod,state='readonly')
        self.comboxlist_1["values"] = tuple(Mycheck.Get_type)
        self.comboxlist_1.bind("<<ComboboxSelected>>", self.Action_post)
        self.label_1.pack(side=LEFT, expand=0, fill=NONE)
        self.comboxlist_1.pack(side=LEFT, expand=0, fill=NONE)

        self.label_2 = Label(self.frmleft_1_2, text="请求地址")
        self.EntA_1 = Entry(self.frmleft_1_2, width=49,highlightcolor='red', highlightthickness=1,textvariable=Ent_C_Top_url,font=("consolas",10))
        self.label_2.pack(side=LEFT, expand=0, fill=NONE)
        self.EntA_1.pack(side=LEFT, expand=1, fill=X)

        self.label_3 = Label(self.frmleft_1_3, text="请求路径")
        self.EntA_2 = Entry(self.frmleft_1_3, width=49,highlightcolor='red', highlightthickness=1,textvariable=Ent_C_Top_path,font=("consolas",10))
        self.label_3.pack(side=LEFT, expand=0, fill=NONE)
        self.EntA_2.pack(side=LEFT, expand=1, fill=X)
    
    def CreateThird(self):
        self.frmleft_2_1 = Frame(self.frmleft_2, width=420, height=260, bg='whitesmoke')
        self.frmleft_2_2 = Frame(self.frmleft_2, width=100, height=260, bg='whitesmoke')
        self.frmleft_2_1.pack(side=LEFT, expand=1, fill=BOTH)
        self.frmleft_2_2.pack(side=RIGHT, expand=0, fill=Y)

        # 表格
        self.treeview_1 = ttk.Treeview(self.frmleft_2_1, height=13, show="headings", columns=self.columns)
        # 表示列,不显示
        self.treeview_1.column("字段", width=120, anchor='w')
        self.treeview_1.column("值", width=300, anchor='w')
        # 显示表头
        self.treeview_1.heading("字段", text="字段")
        self.treeview_1.heading("值", text="值")
        # 双击左键进入编辑
        self.treeview_1.bind('<Double-Button-1>', self.set_cell_value)
        self.treeview_1.pack(expand=1, fill=BOTH)

        self.checkbutton_1 = Button(self.frmleft_2_2, text='发   送', width=10, activebackground = "blue", command=lambda : thread_it(self._request))
        self.checkbutton_2 = Button(self.frmleft_2_2, text='生成EXP', width=10, activebackground = "blue", command=lambda : createexp.show())
        self.checkbutton_3 = Button(self.frmleft_2_2, text='<-还原', width=10, activebackground = "red", command=self.reUrl)

        self.checkbutton_4 = Button(self.frmleft_2_2, text='<-添加', width=10, command=self.newrow)
        self.checkbutton_5 = Button(self.frmleft_2_2, text='<-删除', width=10, command=self.deltreeview)
        self.checkbutton_6 = Button(self.frmleft_2_2, text='清空->', width=10, command=lambda : delText(self.Text_response))
        self.checkbutton_7 = Button(self.frmleft_2_2, text='渲染->', width=10, command=lambda : open_html('./EXP/response.html'))

        self.checkbutton_1.grid(row=0, column=0, padx=1, pady=1, sticky='n')
        self.checkbutton_2.grid(row=1, column=0, padx=1, pady=1, sticky='n')
        self.checkbutton_3.grid(row=2, column=0, padx=1, pady=1, sticky='n')
        self.checkbutton_4.grid(row=3, column=0, padx=1, pady=1, sticky='n')
        self.checkbutton_5.grid(row=4, column=0, padx=1, pady=1, sticky='n')
        self.checkbutton_6.grid(row=5, column=0, padx=1, pady=1, sticky='n')
        self.checkbutton_7.grid(row=6, column=0, padx=1, pady=1, sticky='n')
        # 写入数据
        for i in range(min(len(self.Type),len(self.Value))):
            self.treeview_1.insert('', 
                                i, 
                                iid='I00'+str(i+1),
                                values=(self.Type[i], 
                                self.Value[i]))

    def CreateFourth(self):
        self.Text_post = scrolledtext.ScrolledText(self.frmleft_3, font=("consolas", 10), width=62, height=17, undo = True)
        self.Text_post.pack(expand=1, fill=BOTH)

    def CreateFivth(self):
        self.Text_response = scrolledtext.ScrolledText(self.frmright,font=("consolas", 10), width=76, height=40, undo = True)
        self.Text_response.pack(expand=1, fill=BOTH)
        self.Text_response.configure(state="disabled")

    def Action_post(self, *args):
        if Ent_C_Top_reqmethod.get() == 'POST' or Ent_C_Top_reqmethod.get() == 'PUT':
            self.Type.append('Content-Type')
            self.Value.append('application/x-www-form-urlencoded')
            self.treeview_1.insert('', len(self.Type)-1, values=(self.Type[len(self.Type)-1], self.Value[len(self.Type)-1]))
            self.treeview_1.update()
        else:
            for index in self.treeview_1.get_children():
                if self.treeview_1.item(index, "values")[0] == 'Content-Type':
                    self.treeview_1.delete(index)
                    self.Type[int(index.replace('I00',''))-1] = None
                    self.Value[int(index.replace('I00',''))-1] = None

    def newrow(self):
        self.Type.append('字段')
        self.Value.append('值')
        #解决BUG, insert函数如果不指定iid, 则会自动生成item标识, 此操作不会因del而回转生成
        try:
            self.treeview_1.insert('', 'end',
                            iid='I00'+str(len(self.Type)),
                            values=(self.Type[len(self.Type)-1], 
                            self.Value[len(self.Type)-1]))
            self.treeview_1.update()
        except Exception as e:
            self.Type.pop()
            self.Value.pop()

    def deltreeview(self):
        #index_to_delete = []
        for self.item in self.treeview_1.selection():
            self.treeview_1.delete(self.item)
            self.Type[int(self.item.replace('I00',''))-1] = None
            self.Value[int(self.item.replace('I00',''))-1] = None
            #index_to_delete.append(int(self.item.replace('I00',''))-1)
        
        #self.Type = [self.Type[i] for i in range(0, len(self.Type), 1) if i not in index_to_delete]
        #self.Value = [self.Value[i] for i in range(0, len(self.Value), 1) if i not in index_to_delete]
            
    #双击编辑事件
    def set_cell_value(self, event):
        for self.item in self.treeview_1.selection():
        #item = I001
            item_text = self.treeview_1.item(self.item, "values")
            #a = self.treeview_1.item(self.item)
	
        #print(item_text[0:2])  # 输出所选行的值
        # 列
        self.column= self.treeview_1.identify_column(event.x)
        #row = self.treeview_1.identify_row(event.y)
        # 行
        cn = int(str(self.column).replace('#',''))
        rn = math.floor(math.floor(event.y-25)/18)+1
        #rn = int(str(row).replace('I',''))
        self.entryedit = Text(self.frmleft_2_1, font=("consolas",10))
        self.entryedit.insert(INSERT, item_text[cn-1])
        self.entryedit.bind('<FocusOut>',self.saveedit)
        self.entryedit.place(x=(cn-1)*self.treeview_1.column("字段")["width"],
                        y=25+(rn-1)*18,width=self.treeview_1.column(self.columns[cn-1])["width"],
                        height=18)
        
    #文本失去焦点事件
    def saveedit(self, event):
        try:
            self.treeview_1.set(self.item, column=self.column, value=self.entryedit.get(0.0, "end"))
            a = self.treeview_1.set(self.item)
            if self.column.replace('#','') == '1':
                self.Type[int(self.item.replace('I00',''))-1] = self.entryedit.get(0.0, "end").replace('\n','')
            elif self.column.replace('#','') == '2':
                self.Value[int(self.item.replace('I00',''))-1] = self.entryedit.get(0.0, "end").replace('\n','')

        except Exception as e:
            pass
        finally:
            self.entryedit.destroy()

    def handle_post(self,data_post):
        data_dic = {}
        for i in data_post.split('&'):
            j = i.split('=', 1)
            data_dic.update({j[0]:j[1]})
        return data_dic

    def handle_path(self,path):
        #return ['path','path','path']
        path_list = []
        str1= re.findall('=(.*?)&', path+'&') #返回列表组成字符串
        for i in str1:
            path_tmp = path
            path_tmp = path_tmp.replace(i,i+'\'')
            path_list.append(path_tmp.strip('&'))
        return path_list
        #print(path_list)

    def _request(self):
        self.headers = {}
        self.TIMEOUT = 5
        self.Action = Ent_C_Top_reqmethod.get()
        self.url = Ent_C_Top_url.get().strip('\n') + Ent_C_Top_path.get().strip('\n')
        self.data_post = self.Text_post.get(1.0, "end").strip('\n')
        if self.url:
            pass
        else:
            messagebox.showinfo(title='提示', message='请输入目标地址!')
            return

        for index in self.treeview_1.get_children():
            item_text = self.treeview_1.item(index, "values")

            self.headers.update({item_text[0].strip('\n'):item_text[1].strip('\n')})
        #print(globals())
        self.Text_response.configure(state="normal")
        self.Text_response.delete('1.0','end')
        try:
            if self.Action == 'GET':
                self.response = requests.get(url=self.url,
                                    headers=self.headers,
                                    timeout=self.TIMEOUT,
                                    verify=False,
                                    allow_redirects=False)

            elif self.Action == 'POST':
                #POST数据处理
                if self.headers['Content-Type'] == 'application/x-www-form-urlencoded':
                    self.response = requests.post(url=self.url,
                                                headers=self.headers,
                                                #data=self.handle_post(self.data_post),
                                                data=self.data_post,
                                                timeout=self.TIMEOUT,
                                                verify=False,
                                                allow_redirects=False)
                    
                else:
                    self.response = requests.post(url=self.url,
                                                headers=self.headers,
                                                data=self.data_post,
                                                timeout=self.TIMEOUT,
                                                verify=False,
                                                allow_redirects=False)

            elif self.Action == 'PUT':
                self.response = requests.put(url=self.url,
                                                headers=self.headers,
                                                data=self.data_post,
                                                timeout=self.TIMEOUT,
                                                verify=False,
                                                allow_redirects=False)

            elif self.Action == 'DELETE':
                self.response = requests.delete(url=self.url,
                                                headers=self.headers,
                                                timeout=self.TIMEOUT,
                                                verify=False,
                                                allow_redirects=False)
            else:
                messagebox.showinfo(title='提示', message='暂不支持该方法!')
                return
            self.rawdata = dump.dump_all(self.response,
                                        request_prefix=b'',
                                        response_prefix=b'').decode('utf-8','ignore')
            self.Text_response.delete('1.0','end')
            self.Text_response.insert(INSERT, self.rawdata)
            
            # 转码
            text = self.response.content.decode('utf-8','ignore')
            # 保存
            with open('./EXP/response.html','w',encoding='utf-8') as f:
                f.write(text)
                
        except requests.exceptions.Timeout as error:
            messagebox.showinfo(title='请求超时', message=error)
        except requests.exceptions.ConnectionError as error:
            messagebox.showinfo(title='请求错误', message=error)
        except KeyError as error:
            messagebox.showinfo(title='提示', message='POST请求需要加上 Content-Type 头部字段!')
        except Exception as error:
            messagebox.showinfo(title='错误', message=error)
        finally:
            self.Text_response.configure(state="disabled")

    def reUrl(self):
        Ent_C_Top_reqmethod.set('GET')
        Ent_C_Top_url.set('http://httpbin.org')
        Ent_C_Top_path.set('/ip')

    def check_sql(self):
        url_list = []
        data_list = []
        url = Ent_C_Top_url.get().strip('\n') + Ent_C_Top_path.get().strip('\n')
        method = Ent_C_Top_reqmethod.get().lower()
        data = mycheck.Text_post.get('0.0','end').strip('\n').replace('\n','\\n')
        header = dict(zip(mycheck.Type, mycheck.Value))
        headers = {}
        for key, value in header.items():
            if key and value:
                headers.update({key : value})

        if method == 'get':
            if '?' not in url:
                messagebox.showinfo(title='提示', message='没有存在参数!')
                return
            path = url[url.index('?')+1:]
            url_http = url[:url.index('?')]+'?'

            temp_path = path.split('&')
            for index in range(len(temp_path)):
                temp_list1 = temp_path.copy()
                temp_list1[index] = temp_path[index] + '\'' 
                url_list.append(url_http+'&'.join(temp_list1) )

            Ss = Sql_scan(headers, TIMEOUT=3)
            dbms_type = list(Ss.rules_dict.keys())
            for url_sql in url_list:
                try:
                    html = Ss.urlopen_get(url_sql)
                    if html == '':
                        continue
                    for dbms in dbms_type:
                        if Ss.check_sql_exis(html, Ss.rules_dict[dbms]):
                            messagebox.showinfo(title='提示', message='数据库类型: ' + dbms + '\n' + '注入参数: ' + url_sql)
                            return
                except Exception as e:
                    continue
            #messagebox.showinfo(title='提示', message='不存在SQL注入!')
            messagebox.showinfo(title='错误', message=str(sys.path))

        elif method == 'post':
            if headers['Content-Type'] == 'application/x-www-form-urlencoded':
                temp_data = data.split('&')
                for index in range(len(temp_data)):
                    temp_list2 = temp_data.copy()
                    temp_list2[index] = temp_data[index] + '\'' 
                    data_list.append('&'.join(temp_list2))

                Ss = Sql_scan(headers, TIMEOUT=3)
                dbms_type = list(Ss.rules_dict.keys())
                for data in data_list:
                    try:
                        html = Ss.urlopen_post(url,data)
                        if html == '':
                            continue
                        for dbms in dbms_type:
                            if Ss.check_sql_exis(html, Ss.rules_dict[dbms]):
                                messagebox.showinfo(title='提示', message='数据库类型: ' + dbms + '\n' + '注入数据: ' + data)
                                return
                    except Exception as e:
                        continue
                messagebox.showinfo(title='提示', message='不存在SQL注入!')
                
            elif headers['Content-Type'] == 'application/json':
                data = mycheck.Text_post.get('0.0','end').strip('\n').replace('\n','\\n')
                try:
                    data_dict = json.loads(data)
                    data_key = list(data_dict.keys())
                    data_list = []
                    for index in data_key:
                        if type(data_dict[index]) == type('str'):
                            temp_dict = data_dict.copy()
                            temp_dict[index] = data_dict[index] + '\''
                            data_list.append(temp_dict)
                except Exception as e:
                    messagebox.showinfo(title='错误', message='json解析失败')
                    return

                Ss = Sql_scan(headers, TIMEOUT=3)
                dbms_type = list(Ss.rules_dict.keys())
                for data in data_list:
                    try:
                        html = Ss.urlopen_post(url,json.dumps(data))
                        if html == '':
                            continue
                        for dbms in dbms_type:
                            if Ss.check_sql_exis(html, Ss.rules_dict[dbms]):
                                messagebox.showinfo(title='提示', message='数据库类型: ' + dbms + '\n' + '注入数据: ' + data)
                                return
                    except Exception as e:
                        continue
                messagebox.showinfo(title='提示', message='不存在SQL注入!')
        else:
            pass

    def start(self):
        self.CreateFrm()
        self.CreateFirst()
        self.CreateSecond()
        self.CreateThird()
        self.CreateFourth()
        self.CreateFivth()

#运行状态线程类
class Job(threading.Thread):
    def __init__(self,*args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()   # 用于暂停线程的标识
        self.__flag.set()    # 设置为True
        self.__running = threading.Event()   # 用于停止线程的标识
        self.__running.set()   # 将running设置为True
    def run(self):
        while self.__running.isSet():
            self.__flag.wait()   # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            wait_running()
    def pause(self):
        self.__flag.clear()   # 设置为False, 让线程阻塞
    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞
    def stop(self):
        self.__flag.set()    # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()    # 设置为False

###全局函数定义###
#调用checkbutton按钮
'''
def callCheckbutton(x,i):
    if MyGUI.var[i].get() == 1:
        try:
            for index in range(len(MyGUI.var)):
                if index != i:
                    MyGUI.var[index].set(0)
            MyGUI.vuln = importlib.import_module('.%s'%x,package='POC')
            MyGUI.Checkbutton_text = x
            print('[*] %s 模块已准备就绪!'%x)
        except Exception as e:
            print('[*]异常对象的内容是:%s'%e)
    else:
        MyGUI.vuln = None
        print('[*] %s 模块已取消!'%x)
#创建POC脚本选择Checkbutton
def Create(frm, x, i):
    MyGUI.threadLock.acquire()
    if int(MyGUI.row) > 18:
        MyGUI.row = 1
    button = Checkbutton(frm,text=x,command=lambda:callCheckbutton(x,i),variable=MyGUI.var[i])
    button.grid(row=MyGUI.row,sticky=W)
    #print(x+'加载成功!')
    MyGUI.row += 1
    MyGUI.threadLock.release()

#填充线程列表,创建多个存储POC脚本的界面, 默认为1, 2, 3, 4
def CreateThread():
    temp_list = []
    for i in range(1,len(MyGUI.scripts)+1):
        temp_list.append(str(math.ceil(i/18)))
    temp_dict = dict(zip(MyGUI.scripts,temp_list))

    for i in range(len(MyGUI.scripts)):
        #scripts_name = scripts[i]
        thread = threading.Thread(target=Create,
        args=(gui.frms['frmD_'+ temp_dict[MyGUI.scripts[i]]],
        MyGUI.scripts[i], i))

        thread.setDaemon(True)
        MyGUI.threadList.append(thread)

#加载POC文件夹下的脚本
def LoadPoc():
    try:
        for _ in glob.glob('POC/*.py'):
            script_name = os.path.basename(_).replace('.py', '')
            if script_name == '__init__':
                continue
            i = script_name[0].upper()
            if i not in MyGUI.uppers:
                MyGUI.uppers.append(i)
            MyGUI.scripts.append(script_name)
            m = IntVar()
            MyGUI.var.append(m)
        #去重
        MyGUI.uppers = list(set(MyGUI.uppers))
        #排序
        MyGUI.uppers.sort()
        for i in MyGUI.uppers:
            #fr1=Frame(MyGUI.frmD, width=290, height=580, bg='whitesmoke') #创建选项卡的容器框架
            MyGUI.frms['frmD_'+i] = Frame(MyGUI.frmD, width=290, height=580, bg='whitesmoke')
            MyGUI.note1.add(MyGUI.frms['frmD_'+i], text=i) #装入框架到选项卡
        
        
        #CreateThread()

        #for t in MyGUI.threadList:
        #    t.start()
    except Exception as e:
        messagebox.showinfo('提示','请勿重复加载')
'''
#加载EXP文件夹下的脚本
def LoadEXP():
    global exp_scripts
    exp_scripts = exp_scripts[0:1]#清除脚本列表
    for _ in glob.glob('EXP/*.py'):
        script_name = os.path.basename(_).replace('.py', '')
        if script_name != 'ALL':
            exp_scripts.append(script_name)
    exp_scripts.remove('__init__')

def RefreshEXP():
    global exp_scripts_cve,exp_scripts
    try:
        LoadEXP()
        exp_scripts_cve = exp_scripts_cve[0:1]
        x = exp.comboxlist_1_3.get()
        for func in dir(myexp_vuln.__dict__[x]):#获取实际导入的EXP对象
            if not func.startswith("__") and not func.startswith("_"):
                exp_scripts_cve.append(func)#设置具体的CVE漏洞
        exp.comboxlist_1_3["values"] = tuple(exp_scripts)
        exp.comboxlist_1_3_1["values"] = tuple(exp_scripts_cve)#设置具体的CVE漏
    #except AttributeError:
    #    messagebox.showinfo('提示','当前还未加载脚本对象!')
    except Exception as e:
        messagebox.showinfo('错误',str(e))

#漏洞利用界面根据漏洞类型显示对应的CVE
def bind_combobox(*args):
    global exp_scripts_cve,myexp_vuln
    try:
        exp_scripts_cve = ['ALL']
        x = exp.comboxlist_1_3.get()
        myexp_vuln = importlib.import_module('.%s'%x,package='EXP')
        #print(MyEXP.vuln.__dict__)
        for func in dir(myexp_vuln.__dict__[x]):#获取实际导入的EXP对象
        #for func in dir(MyEXP.vuln.__dict__[x.lower()]):
            if not func.startswith("__") and not func.startswith("_"):
                exp_scripts_cve.append(func)#设置具体的CVE漏洞
        exp.comboxlist_1_3_1["values"] = tuple(exp_scripts_cve)#设置具体的CVE漏洞
        print('[*]%s模块已准备就绪!'%x)
    except KeyError:
        exp.comboxlist_1_3_1["values"] = tuple(exp_scripts_cve)#设置具体的CVE漏洞
        myexp_vuln = importlib.import_module('.%s'%x,package='EXP')
        print('[*]%s模块已准备就绪!'%x)
    except Exception as e:
        print('[*]异常对象的内容是:%s'%e)
    finally:
        Ent_B_Top_vulmethod.set("ALL")

def bind_combobox_3(*args):
    x = exp.comboxlist_4.get()
    if x == 'False':
        Ent_B_Bottom_Left_cmd.set('echo '+ GlobalVar.get_value('flag'))
    else:
        Ent_B_Bottom_Left_cmd.set('whoami')


def thread_it(func, **kwargs):
    exp.thread = threading.Thread(target=func, kwargs=kwargs)
    exp.thread.setDaemon(True)
    #启动
    exp.thread.start()

def stop_thread(thread):
    if thread is not None:
        try:
            _async_raise(thread.ident, SystemExit)
            #self.wait_running_job.stop()
            print("[*]已停止运行")
        except Exception as e:
            messagebox.showinfo('提示',e)

#当前运行状态
def wait_running():
    MyGUI.wait_index = 0
    list = ["\\", "|", "/", "—"]
    gui.TexA2.configure(state="normal")
    while True:
        index = MyGUI.wait_index % 4
        gui.TexA2.insert(INSERT,list[index])
        time.sleep(0.25)
        gui.TexA2.delete('1.0','end')
        MyGUI.wait_index = MyGUI.wait_index + 1

#终止子线程
def _async_raise(tid, exctype):
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

#返回分隔符号函数
def Separator_(str_):
    index = 104 - len(str_)
    left = math.ceil(index/2)
    right = math.floor(index/2)
    return '-'*left + str_ + '-'*right

#显示线程运行状态
def ShowPython():
    try:
        print('[*]'+gui.t.getName()+' 运行状态: '+ str(gui.t.isAlive()))
        print('[*]'+gui.t2.getName()+' 运行状态: '+ str(gui.t2.isAlive()))
    except AttributeError:
        messagebox.showinfo(title='提示', message='进程还未启动')
    except Exception as e:
        messagebox.showinfo(title='错误', message=e)
        
def save_result():
    #if MyGUI.vul_name != '' and MyGUI.wbswitch == 'true':
    if MyGUI.wbswitch == 'true':
        timestr = time.strftime("%Y%m%d_%H%M%S")#获取当前时间
        print('[*]已保存检测结果 -> %s_%s.xlsx'%(MyGUI.vul_name,timestr))
        MyGUI.wb.save('./result/%s_%s.xlsx'%(MyGUI.vul_name,timestr))
        #不清空数据
        # MyGUI.wb = None
        # MyGUI.ws = None
    else:
        print('[-]未找到批量检测结果, 请先执行脚本测试!')
        
# 重载脚本函数
def ReLoad():
    try:
        MyGUI.vuln = importlib.reload(MyGUI.vuln)
        print('[*]加载成功!')
    except Exception as e:
        messagebox.showinfo(title='提示', message='重新加载失败')
        return

# 切换界面函数
def switchscreen(frame):
    for screen in MyGUI.screens:
        # grid布局 grid_remove()
        # pack布局 pack_forget()
        screen.pack_forget()
    frame.pack(side=BOTTOM, expand=1, fill=BOTH)
    if frame == gui.frmPOC:
        # 输出重定向到POC界面
        sys.stdout = TextRedirector(gui.TexB, "stdout")
    elif frame == gui.frmEXP:
        # 输出重定向到EXP界面
        sys.stdout = TextRedirector(exp.TexBOT_1_2, "stdout", index="exp")

# 进度条自动增长函数
def autoAdd():
    from util.fun import randomInt
    thread_list = GlobalVar.get_value('thread_list')
    flag = round(400/len(thread_list), 2)
    #if len(thread_list) == 1:
    #    return
    #标志位
    index_list = [index for index in range(len(thread_list))]
    while True:
        thread_num = len(index_list)
        #使用倒叙遍历列表
        for index in range(len(index_list)-1, -1, -1):
            #完成
            #if thread_list[index].done() == True:
            if thread_list[index_list[index]]._state == 'FINISHED':
                #删除标志位
                del index_list[index]
        #每次循环遍历所增长的进度
        exp.frame_progress.pBar["value"] = exp.frame_progress.pBar["value"] + (thread_num - len(index_list)) * flag
        #全部执行完成
        if len(index_list) == 0:
            exp.frame_progress.pBar["value"] = 1000
            break
        time.sleep(randomInt(1,3))

#取消未执行的任务
def CancelThread():   
    thread_list = GlobalVar.get_value('thread_list')
    if len(thread_list) == 0:
        messagebox.showinfo(title='提示', message='没有正在运行的任务~')
        return
    index = 0
    try:
        for task in thread_list:
            if task.cancel() == True:
                index += 1
        messagebox.showinfo(title='提示', message="总共有%s个任务, 成功取消%s个任务"%(len(thread_list),str(index)))
    except TypeError as e:
        messagebox.showinfo(title='错误', message='TypeError: '+ str(e))
    except Exception as e:
        messagebox.showinfo(title='错误', message=str(e))

#漏洞利用界面执行命令函数
def exeCMD(**kwargs):
    from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED,CancelledError
    if myexp_vuln == None:
        messagebox.showinfo(title='提示', message='还未选择模块')
        return
    # 命令执行检测代理
    if Proxy_CheckVar1.get() == 0:
        if messagebox.askokcancel('提示','程序检测到未挂代理进行扫描,请确认是否继续?') == False:
            print("[-]扫描已取消!")
            return
    #开始标志
    #exp.color_switch('green')
    #获取记录条数
    try:
        with open(rootPath+'/data/scandb.json', mode='r', encoding='utf-8') as f:
            filejson = [i for i in f.readlines() if i != '\n']
        temp = len(filejson)
    except Exception:
        temp = 0
    start = time.time()
    #初始化全局子线程列表
    pool = ThreadPoolExecutor(kwargs['pool_num'])
    kwargs['pool'] = pool
    GlobalVar.set_value('thread_list', [])
    #进度条初始化
    exp.frame_progress.pBar["value"] = 0
    print("[*]开始执行测试: %s"%kwargs['url'])
    #单模块测试
    if kwargs['url']:
        #单目标执行
        try:
            print("[*]正在装填线程列表, 即将开始测试!")
            myexp_vuln.check(**kwargs)
            #进度条开始增长
            exp.frame_progress.pBar["value"] = exp.frame_progress.pBar["value"] + 600
            thread_it(autoAdd)
            wait(GlobalVar.get_value('thread_list'), return_when=ALL_COMPLETED)
            
            for future in GlobalVar.get_value('thread_list'):
                try:
                    #结果不为None
                    if future.result():
                        i = future.result().split("|")
                        #去除取消掉的future任务
                        if future.cancelled() == False:
                            if 'success' == i[3]:
                                i = future.result().split("|")
                                #根据返回值生成一条扫描记录
                                scan_one_record = ScanRecord(
                                    target = i[0],
                                    appName = i[1],
                                    pocname = i[2],
                                    last_status = i[3],
                                    last_time = i[4],
                                )
                                #插入前+1
                                temp += 1
                                #插入扫描记录
                                myvuldatabase.tree.insert("","end",values=(
                                    temp,
                                    scan_one_record.target, 
                                    scan_one_record.appName,
                                    scan_one_record.pocname,
                                    scan_one_record.last_status,
                                    scan_one_record.last_time,
                                    )
                                )
                except CancelledError:
                    continue
        except Exception as e:
            print('出现错误: %s'%e)
        #结束
        end = time.time()
        print('[*]共花费时间：{} 秒'.format(seconds2hms(end - start)))
    #多模块测试
    elif myurls.TexA.get('0.0','end').strip('\n'):
        #去空处理
        file_list = [i for i in myurls.TexA.get('0.0','end').split("\n") if i != '']
        #存储字典参数列表
        dict_list = []
        name = myexp_vuln.__name__.replace('EXP.','')
        for url in file_list:
            dict_temp = kwargs.copy()
            dict_temp['url'] = url.strip('/')
            dict_list.append(dict_temp)
        #装填非多线程
        print("[*]正在装填线程列表, 即将开始测试!")
        #600=1000-400
        flag = round(600/len(dict_list), 2)
        for kwargs in dict_list:
            myexp_vuln.check(**kwargs)
            exp.frame_progress.pBar["value"] = exp.frame_progress.pBar["value"] + flag
        #进度条开始增长,有个问题:当发送的payload大于线程池数量时,当剩下的payload全部装填满线程池时,进度条才会涨...
        #解决办法:进度条分两部分，如长度共1000，前600分给填充线程池，后400分给判断是否完成
        thread_it(autoAdd)
        #阻塞主线程，直到满足条件
        #FIRST_COMPLETED（完成1个）
        #FIRST_EXCEPTION（报错1个）
        #ALL_COMPLETED（完成所有）
        wait(GlobalVar.get_value('thread_list'), return_when=ALL_COMPLETED)
        
        #根据结果生成表格
        tb = pt.PrettyTable()
        tb.field_names = ["Index", "Type", "Result"]
        tb.align['Type'] = 'l'
        tb.align['Result'] = 'l'
        
        #总共加载的poc数
        total_num = 1
        #成功次数
        success_num = 0
        #失败次数
        fail_num = 0
        #没有结果次数
        noresult_num = 0
        #成功列表
        result_list = []
        for future in GlobalVar.get_value('thread_list'):
            try:
                if future.result():
                    i = future.result().split("|")
                    #去除取消掉的future任务
                    if future.cancelled() == False:
                        if future.result() is None:
                            noresult_num += 1
                            tb.add_row([str(total_num), name, 'None, Notice:function no return'])
                        else:
                            if 'success' == i[3]:
                                success_num += 1
                                result_list.append('[+] '+i[0]+'   '+i[2]+' -> '+i[3])
                                #根据返回值生成一条扫描记录
                                scan_one_record = ScanRecord(
                                    target = i[0],
                                    appName = i[1],
                                    pocname = i[2],
                                    last_status = i[3],
                                    last_time = i[4],
                                )
                                #插入前+1
                                temp += 1
                                #插入扫描记录
                                myvuldatabase.tree.insert("","end",values=(
                                    temp,
                                    scan_one_record.target,
                                    scan_one_record.appName,
                                    scan_one_record.pocname,
                                    scan_one_record.last_status,
                                    scan_one_record.last_time,
                                    )
                                )               
                            else:
                                fail_num += 1
                            tb.add_row([str(total_num), name, i[0]+'   '+i[2]+' -> '+i[3]])
                        total_num += 1
            except CancelledError:
                continue
        tb.add_row(['count', name, 'total: %s , success: %s , fail: %s , none: %s'%(str(total_num-1),str(success_num),str(fail_num),str(noresult_num))])
        print(tb)
        for sucess_str in result_list:
            color(sucess_str, 'green')
        with open('./EXP/output.html', "wb") as f:
            f.write(tb.get_html_string().encode('utf8'))
        #结束
        end = time.time()
        print('[*]共花费时间：{} 秒'.format(seconds2hms(end - start)))
        if success_num == 0:
            print('[-]未找到漏洞(-Λ-)')
            #messagebox.showinfo(title='结果', message='未找到漏洞(-Λ-)')
        else:
            messagebox.showinfo(title='结果', message='共找到 %s 个漏洞(-v-)'%str(success_num))
    else:
        color('[*]请输入目标URL!','red')
        color('[*]请输入目标URL!','yellow')
        color('[*]请输入目标URL!','blue')
        color('[*]请输入目标URL!','green')
        color('[*]请输入目标URL!','orange')
        color('[*]请输入目标URL!','pink')
        color('[*]请输入目标URL!','cyan')
    #结束标志
    #exp.color_switch('red')
    exp.frame_progress.pBar["value"] = 1000
    #保存本次扫描结果到漏洞库存中
    myvuldatabase.save_tree()
    #渲染颜色
    myvuldatabase.render_color()
    #关闭线程池
    pool.shutdown()

#退出时执行的函数
def callbackClose():
    if messagebox.askokcancel('提示','要退出程序吗?') == True:
        try:
            #笔记保存
            mynote.save()
            #保存漏洞库存结果
            myvuldatabase.save_tree()
            #保存代理池
            my_proxy_pool.save_tree()
            #程序异常日志保存
            mydebug.save()
            #sys.exit(0)
            #gui.root.destroy()
        except Exception:
            #addToClipboard(save_data)
            messagebox.showerror(title='保存文件错误')
        finally:
            sys.exit(0)

if __name__ == "__main__":
    gui = MyGUI()
    #定义Treeview每个组件高度
    s = ttk.Style()
    #repace 40 with whatever you need
    s.configure('Treeview', rowheight=18)
    s.configure('red.TSeparator',background='red')
    #导入变量
    from settings import Proxy_type,Proxy_CheckVar1,Proxy_CheckVar2,Proxy_addr,Proxy_port, rootPath, PojectPath,\
        Ent_A_Top_thread, Ent_A_Top_Text, \
        Ent_B_Top_url,Ent_B_Top_cookie,Ent_B_Top_vulname,Ent_B_Top_vulmethod,Ent_B_Top_funtype,Ent_B_Top_timeout,Ent_B_Top_retry_time,Ent_B_Top_retry_interval,Ent_B_Top_thread_pool,Ent_B_Bottom_Left_cmd,Ent_B_Bottom_terminal_cmd, \
        Ent_C_Top_url,Ent_C_Top_path,Ent_C_Top_reqmethod,Ent_C_Top_vulname,Ent_C_Top_cmsname,Ent_C_Top_cvename,Ent_C_Top_version,Ent_C_Top_info,Ent_C_Top_template, \
        Ent_Cmds_Top_type,Ent_Cmds_Top_typevar, \
        Ent_yso_Top_type,Ent_yso_Top_class,Ent_yso_Top_cmd, \
        TCP_Debug_IP,TCP_Debug_PORT,TCP_Debug_PKT_BUFF_SIZE, \
        variable_dict,Proxy_web, \
        exp_scripts,exp_scripts_cve,myexp_vuln

    #初始化全局变量
    GlobalVar._init()
    #随机数
    flag = random_name(18)
    GlobalVar.set_value('flag', flag)
    #初始化配置文件
    settings_vuln = importlib.import_module('.GlobSettings',package='POC')
    GlobalVar.set_value('settings_vuln', settings_vuln)
    GlobalVar.set_value('screens', MyGUI.screens)
    #初始化全局代理变量
    os.environ['HTTP_PROXY'] = ''
    os.environ['HTTPS_PROXY'] = ''
    #生初始化漏洞扫描界面    
    gui.start()
    #生成漏洞利用界面
    exp = MyEXP(gui)
    exp.start()
    GlobalVar.set_value('exp', exp)
    #生成漏洞测试界面
    mycheck = Mycheck(gui)
    mycheck.start()
    GlobalVar.set_value('mycheck', mycheck)
    #生成漏洞笔记界面
    from core import Loadfile, CodeFile, TopProxy, CreateExp, Mynote, VulDatabase, Proxy_pool, Debug, Terlog, Tools, Thread, Zichanspace, Yufa_pool
    from module import ScanRecord
    mynote = Mynote(gui)
    mynote.start()
    GlobalVar.set_value('mynote', mynote)
    #多目标输入界面
    myurls = Loadfile(gui)
    myurls.hide()
    GlobalVar.set_value('myurls', myurls)
    #漏洞工具
    mytools = Tools(gui)
    mytools.start()
    GlobalVar.set_value('mytools', mytools)
    #威胁分析
    mythread = Thread(gui)
    mythread.start()
    GlobalVar.set_value('mythread', mythread)
    #终端日志
    myterlog = Terlog(gui)
    myterlog.start()
    GlobalVar.set_value('myterlog', myterlog)
    #程序异常日志界面
    mydebug = Debug(gui)
    mydebug.start()
    GlobalVar.set_value('mydebug', mydebug)
    #漏洞库界面
    myvuldatabase = VulDatabase(gui)
    myvuldatabase.start()
    GlobalVar.set_value('myvuldatabase', myvuldatabase)
    #资产空间界面
    myzichanspace = Zichanspace(gui)
    myzichanspace.start()
    GlobalVar.set_value('myzichanspace', myzichanspace)
    # #多目标输入界面
    # myurls = Loadfile(gui)
    # myurls.hide()
    #设置代理
    myproxy = TopProxy(gui)
    myproxy.hide()
    GlobalVar.set_value('myproxy', myproxy)
    #代理池
    my_proxy_pool = Proxy_pool(gui)
    my_proxy_pool.hide()
    #语法池
    my_yufa_pool = Yufa_pool(gui)
    my_yufa_pool.hide()
    GlobalVar.set_value('my_yufa_pool', my_yufa_pool)
    #生成EXP
    createexp = CreateExp(gui)
    createexp.hide()
    GlobalVar.set_value('createexp', createexp)
    #myyaml = YamlFile(gui)
    #输出重定向
    sys.stdout = TextRedirector(gui.TexB, "stdout")
    #输出类
    # poc = TextRedirector(gui.TexB, "stdout")
    # exp = TextRedirector(gui.TexB, "stdout")
    # sys.stdout = TextRedirector(myterlog.Terlog_note, "stdout")
    #标准错误重定向
    sys.stderr = TextRedirector(mydebug.Debug_note, "stderr")
    #INSERT表示输入光标所在的位置，初始化后的输入光标默认在左上角
    gui.TexB.insert(INSERT, Ent_A_Top_Text.lstrip('\n'))
    #自定义退出函数
    gui.root.protocol("WM_DELETE_WINDOW", callbackClose)
    gui.root.mainloop()