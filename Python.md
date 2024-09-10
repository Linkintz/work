# Python

[TOC]





## 存储类

### 网页

````python
import requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
url=r'https://www.baidu.com/'
response = requests.get(url,headers=headers)#不加头部信息，编码错误
with open('baidu.html',mode='w',encoding='utf-8') as f:
    f.write(response.text)
````

### 图片

~~~python
def saveJpg(img_url,path):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}
    req = requests.get(img_url, headers=headers,timeout=(3,7))# 超时处理+@retry()
    f = open(path, 'wb')
    f.write(req.content)
    f.close	
~~~

### 文本

~~~python
def saveText(name,text):
    f = open(r"D:\txt\\"+name+'.txt', mode='a', encoding='utf-8')
    f.write(text)
    f.write("\n")
    f.close()
~~~

### 压缩文件

~~~python
def getZip(path):#给绝对路径，压缩路径
    # zipfile_name = os.path.basename(path) + '.zip'  #返回当前目录名字+zip，例如123.zip
    zipfile_name = path + '.zip'  # 返回当前目录名字+zip，例如123.zip
    print(zipfile_name)
    zz=zipfile.ZipFile(zipfile_name, 'w',zipfile.ZIP_DEFLATED)
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        print(file_path)
        zz.write(file_path,file)
        if os.path.exists(zipfile_name):  # 检查压缩包是否存在
            pass
~~~

### Excel

~~~python
import openpyxl

def main():
    s_name="123"
    filename=s_name+".xlsx"
    fx=open_or_create(filename)
    fx.create_sheet('111')
    sheets=fx.worksheets
    print(fx.sheetnames)
    sheet=sheets[0]
    sheet.cell(1,1,"123")
    sheet.cell(2,1,"123")

    #fx.remove(sheet)#在使用openpyxl创建excel时，有时会需要将不需要的sheet删除掉，有一下两种办法：
                    # 一：del wb[“sheet_name”]
                    # 二：ws = wb[“sheet_name”]
                    # wb.remove[ws]
    #print(sheets[1].title)
    print(sheet.max_row)
    fx.create_sheet('123')

    print(fx.sheetnames)
    del fx["123"]
    print(fx.sheetnames)
    fx.save(filename)


def open_or_create(filename):
    try:
        f = openpyxl.load_workbook(filename)
    except IOError:
        print("No exit!")
        f = openpyxl.Workbook()
        f.save(filename)
    return f

if __name__ == "__main__":
    main()
~~~

## 输入端

###  输出方式

~~~python
a = '张三'
b = 24
c = 60.0
print('我的名字是%s,年龄%d,体重为%f公斤'%(a,b,c))#整数类型为%d，字符串为%s，浮点型为%f
print(f'我的名字是{a},年龄{b},体重为{c}公斤')#引号前添加 f 或 F 可以在 { 和 } 字符之间输入引用的变量，或字面值的 Python 表达式
~~~

![image-20211120144015261](C:\Users\果果\AppData\Roaming\Typora\typora-user-images\image-20211120144015261.png)

| 符  号 | 描述                                 |
| ------ | ------------------------------------ |
| %c     | 格式化字符及其ASCII码                |
| %s     | 格式化字符串                         |
| %d     | 格式化整数                           |
| %u     | 格式化无符号整型                     |
| %o     | 格式化无符号八进制数                 |
| %x     | 格式化无符号十六进制数               |
| %X     | 格式化无符号十六进制数（大写）       |
| %f     | 格式化浮点数字，可指定小数点后的精度 |
| %e     | 用科学计数法格式化浮点数             |
| %E     | 作用同%e，用科学计数法格式化浮点数   |
| %g     | %f和%e的简写                         |
| %G     | %F 和 %E 的简写                      |
| %p     | 用十六进制数格式化变量的地址         |

## 目录文件

### 遍历当前路径下目录

~~~python
def getPath(path):#当前路径下所有文件夹
    # for root, dirs, files in os.walk(path):
    #     print(root)  # 当前目录路径
    #     # print(dirs)  # 当前路径下所有子目录
    #     # print(files) #当前路径下所有非目录子文件
    fileList = []
    for file in os.listdir(path):
        # print(file)
        file=os.path.join(path, file)
        if os.path.isdir(file):
            file_path = os.path.basename(file)
            fileList.append(file_path)
    return fileList
~~~

### 目录不存在则创建

~~~python
def creatPath(path):
    # if os.path.exists(path):
    #     print('dir exists')
    # else:
    #     print('dir not exists')
    #     os.makedirs(path)
    if not os.path.exists(path):
        os.makedirs(path)
~~~

### 移动当前目录下指定格式文件

~~~python
def moveZip(old_path,new_path):# 移动old_path目录下所有zip文件至new_path
    # old_path=r'F:\dist\dist'
    for file in os.listdir(old_path):
        if file.endswith('.zip'):
            # print(file)
            file_path = os.path.join(old_path, file)
            shutil.move(file_path,new_path)
~~~

---------------------------------

## 技术技巧

### 排除列表中重复数据

方法一：

~~~python
list3 = []
for one in list1:
    if one not in l:
        list3.append(one)
~~~

方法二：

~~~python
list3 = [i for i in list1 if i not in list2]
~~~

### 多线程

~~~python
import threading
threading.Thread(target=saveJpg,args=(i,pathJpg)).start()# target目标函数，args为参数
~~~

### 重试机制

~~~python
from retry import retry
@retry()
def ...# 配合请求函数+超时timeout（）
~~~

## 其他

### xls数据导入oracle

~~~python
import cx_Oracle as oracle
import xlrd

#变量输入
db_napwdb='scott/scott@127.0.0.1:1521/orcl'        # ('账号/密码@ip:端口/数据库实例名')
udate_path=r'C:\Users\果果\Desktop\file.xls.xls'    #数据来源路径
sh_num=0                                           #xls的sheet页
t_name='xiaoqu_tmp'

conn = oracle.connect(db_napwdb)
cursor = conn.cursor()  # 使用cursor()方法获取数据库的操作游标(游标是记录操作哪个库、表、字段、时间等信息)
# cursor=conn.cursor()#使用cursor()方法获取数据库的操作游标(游标是记录操作哪个库、表、字段、时间等信息)
book = xlrd.open_workbook(udate_path)

try:
    sheet1 = book.sheets()[sh_num]
    for i in range(1,sheet1.nrows):
        value = str(tuple(sheet1.row_values(i)))
        sql='insert into '+t_name+' values'+value
        cursor.execute(sql)  # SelectSql可以是其他数据库操作变量,执行sql语句,返回的是影响行数
        conn.commit()  # 提交操作
    conn.close()  # 关闭数据库连接
except oracle.DatabaseError as e:
    print("oracle error %d:%s" % (e.args[0], e.args[1]))  # 捕获异常(如数据库无法连接：ip、端口错误等)
    conn.rollback()  # 报错时回退
    cursor.close()  # 关闭游标
    conn.close()  # 关闭数据库连接

~~~

### 邮件处理

~~~python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

#设置登录及服务器信息
mail_host = 'smtp.qq.com'
mail_user = '1375243349@qq.com'
mail_pass = 'doglovwqxkdvjicd'
sender = '1375243349@qq.com'
receivers = ['1161784596@qq.com']

#设置eamil信息
#添加一个MIMEmultipart类，处理正文及附件
message = MIMEMultipart()
message['From'] = sender
message['To'] = receivers[0]
message['Subject'] = 'nihao'
#推荐使用html格式的正文内容，这样比较灵活，可以附加图片地址，调整格式等
# with open('abc.html','r') as f:
#     content = f.read()
# #设置html格式参数
a='现在要在一个进程中同时由多个邮箱发送邮件。此事不但要注意上面描述的情况外，'

part1 = MIMEText(a,'plain','utf-8')
# #添加一个txt文本附件
# with open('abc.txt','r')as h:
#     content2 = h.read()
# #设置txt参数
# part2 = MIMEText(content2,'plain','utf-8')
# #附件设置内容类型，方便起见，设置为二进制流
# part2['Content-Type'] = 'application/octet-stream'
# #设置附件头，添加文件名
# part2['Content-Disposition'] = 'attachment;filename="abc.txt"'
# #添加照片附件
# with open('1.png','rb')as fp:
#     picture = MIMEImage(fp.read())
#     #与txt文件设置相似
#     picture['Content-Type'] = 'application/octet-stream'
#     picture['Content-Disposition'] = 'attachment;filename="1.png"'
# #将内容附加到邮件主体中
message.attach(part1)
# message.attach(part2)
# message.attach(picture)

#登录并发送
try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host,25)
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(
        sender,receivers,message.as_string())
    print('success')
    smtpObj.quit()
except smtplib.SMTPException as e:
    print('error',e)
~~~

### 打包exe

建议cmd窗口下执行，导入库时指定使用模块，减小exe文件大小，确保pip内有需要模块

~~~python
pyinstaller -F -w  -p F:\python\lib\ -i www.ico weixin.py
~~~

| -h，--help                  | 查看该模块的帮助信息                                         |
| --------------------------- | ------------------------------------------------------------ |
| -F，-onefile                | 产生单个的可执行文件                                         |
| -D，--onedir                | 产生一个目录（包含多个文件）作为可执行程序                   |
| -a，--ascii                 | 不包含 Unicode 字符集支持                                    |
| -d，--debug                 | 产生 debug 版本的可执行文件                                  |
| -w，--windowed，--noconsolc | 指定程序运行时不显示命令行窗口（仅对 Windows 有效）          |
| -c，--nowindowed，--console | 指定使用命令行窗口运行程序（仅对 Windows 有效）              |
| -o DIR，--out=DIR           | 指定 spec 文件的生成目录。如果没有指定，则默认使用当前目录来生成 spec 文件 |
| -p DIR，--path=DIR          | 设置 Python 导入模块的路径（和设置 PYTHONPATH 环境变量的作用相似）。也可使用路径分隔符（Windows 使用分号，Linux 使用冒号）来分隔多个路径 |
| -n NAME，--name=NAME        | 指定项目（产生的 spec）名字。如果省略该选项，那么第一个脚本的主文件名将作为 spec 的名字 |

### GUI编程（图形化交互）

- **Tkinter：** Tkinter 模块(Tk 接口)是 Python 的标准 Tk GUI 工具包的接口 .Tk 和 Tkinter 可以在大多数的 Unix 平台下使用,同样可以应用在 Windows 和 Macintosh 系统里。Tk8.0 的后续版本可以实现本地窗口风格,并良好地运行在绝大多数平台中。
- **wxPython：**wxPython 是一款开源软件，是 Python 语言的一套优秀的 GUI 图形库，允许 Python 程序员很方便的创建完整的、功能健全的 GUI 用户界面。
- **Jython：**Jython 程序可以和 Java 无缝集成。除了一些标准模块，Jython 使用 Java 的模块。Jython 几乎拥有标准的Python 中不依赖于 C 语言的全部模块。比如，Jython 的用户界面将使用 Swing，AWT或者 SWT。Jython 可以被动态或静态地编译成 Java 字节码。

~~~python
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog

def ui_process():
    root =Tk()
    root.title('第一个界面')# 窗口标题
    root.geometry("300x400+50+50")# 窗口大小，+500+500窗口平移

    root.update()  # 一定要刷新界面，否则打印出的值是1
    print("当前窗口的宽度为", root.winfo_width())
    print("当前窗口的高度为", root.winfo_height())


#标签
    L_titile = Label(root,text='个人界面设计',)
    L_titile.config(font='Helvetica -15 bold',fg='blue')
    L_titile.place(x=150,y=20,anchor="center")
    L_author = Label(root, text='作者:你大爷')
    L_author.config(font='Helvetica -10 bold')
    L_author.place(x=230,y=380)

#按钮
    B_0 = Button(root, text="对话框", command=CreatDialog)
    B_0.place(x=90,y=200)
    B_1 = Button(root, text="确定", command=print)
    B_1.place(x=150, y=200)
    B_OK = Button(root,text="创建",command=lambda:button_process(root))
    B_OK.place(x=200,y=200)
    B_NO = Button(root, text="取消")
    B_NO.place(x=250,y=200)

#单选按钮
    v = IntVar()
    R_ONE=Radiobutton(root, text="One", variable=v, 				 value=1,command=lambda:Print_b(1)).place(x=60,y=150)
    R_TWO=Radiobutton(root, text="Two", variable=v, value=2,command=lambda:Print_b(2)).place(x=10,y=150)
#多选按钮
    chk_state_MP3 = BooleanVar()
    chk = Checkbutton(root, text="MP3", var=chk_state_MP3, command=lambda: append_boole('mp3', chk_state_MP3.get()))
    chk.place(x=80, y=150)
    chk_state_mp4 = BooleanVar()
    chk_state_mp4.set(True)  # 默认值
    chk = Checkbutton(root, text="MP4", var=chk_state_mp4, command=lambda: append_boole('mp4', chk_state_mp4.get()))
    chk.place(x=130, y=150)

#滑块
    W = Scale(root, from_=0, to=100,orient=HORIZONTAL)#orient=HORIZONTAL 横向，默认纵向
    W.place(x=50,y=300)
    print(W.get())  #获取滑块值
# 输入框
    Label(root, text='BV号：').place(x=5, y=10)
    E_bv = Entry(root)
    E_bv.place(x=50, y=10)
    print(E_bv.get())# 获取输入框内容
#菜单栏
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=OpenFile)
    filemenu.add_command(label="Save", command=SaveFile)
    # filemenu.add_separator()#分割线
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)
# 多选框控件
    chk_state_MP3 = BooleanVar()
    # chk_state.set(False[Ture])  # 默认值
    chk = Checkbutton(root, text="MP3", var=chk_state_MP3,command=lambda:Print_b(['mp3',chk_state_MP3.get()]))
    chk.place(x=110, y=150)
# 滚动条控件
    scro_txt = Scrollbar(root, width=40)
    # # scro_txt.grid(column=0, row=4)
    scro_txt.place(x=110, y=230)
# 显示与滑钮
    S_0 = Scrollbar(root)
    S_0.pack(side="right", fill="y")# 组件布局方式，guid、pack、place
    P_0 = Listbox(root,yscrollcommand=S_0.set)# 通过绑定，让Scrollbar滑动显示Listbox
    P_0.place(x=220,y=10)
    S_0.config(command=P_0.yview)# 12宽度
    sc_txt('欢迎使用bilibili下载器')

    root.mainloop() #调用组件，进入事件循环

# 显示框显示内容
def sc_txt(pp):
    list = [pp[i:i + 12] for i in range(0, len(pp), 12)]
    for i in list:
        P_0.insert(END, i)
#按钮对应函数入口
def button_process(root):
    #创建消息框
    messagebox.askokcancel('Python Tkinter', '确认创建窗口？')
    messagebox.askquestion('Python Tkinter', "确认创建窗口?")
    messagebox.askyesno('Python Tkinter', '是否创建窗口？')
    messagebox.showerror('Python Tkinter', '未知错误')
    messagebox.showinfo('Python Tkinter', 'hello world')
    messagebox.showwarning('Python Tkinter', '电脑即将爆炸，请迅速离开')
    root1 = Toplevel(root)

def PrintHello():
    print("hello")

def Print_b(a):
    print(a)

#创建对话框
def CreatDialog():
    world = simpledialog.askstring('Python Tkinter', 'Input String', initialvalue = 'Python Tkinter')
    print(world)
    # simpledialog.askinteger()
    # simpledialog.askfloat()

#文件操作的对话框
def OpenFile():
    f = filedialog.askopenfilename(title='打开文件', filetypes=[('Python', '*.py *.pyw'), ('All Files', '*')])
    print(f)
    #可使用os 模块运行文件
def SaveFile():
    f = filedialog.asksaveasfilename(title='保存文件', initialdir='d:\mywork', initialfile='hello.py')
    print(f)
    #可调用OS模块保存
if __name__ == "__main__":
    print("开始")
    ui_process()# 如需调用其他函数，建议放入至ui_process函数内
~~~

### 自动化处理

### 安装第三方库

~~~ text
pip install parsel -i https://pypi.tuna.tsinghua.edu.cn/simple/
~~~

