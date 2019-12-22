from tkinter import *
from sql_base import *
import tkinter.messagebox
from tkinter import ttk
#import pymysql
from PIL import Image,ImageTk
import sqlite3
import time

def center(window, w, h):  # 设置窗口大小且居中
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry("{:.0f}x{:.0f}+{:.0f}+{:.0f}".format(w, h, x, y))


class Main(Frame):
    """主窗口"""
    flag = None
    def __init__(self,user):
        Frame.__init__(self, master=None)
        self.pack(fill=BOTH, expand=YES)
        self.master.geometry("1200x800")
        self.master.title("民航销售管理系统")
        self.frame_top = Frame(self)
        self.frame_top.pack(side="top", fill=X)
        Label(self.frame_top, text="民航销售管理系统", font=("微软雅黑", 30), fg='black', bg='beige').pack(fill=X)
        # im=Image.open("fj.jpg")
        # img=ImageTk.PhotoImage(im)
        # Label(self.frame_top,image=img).pack(fill=X)
        self.frame_bottom = Frame(self)  # 下方frame
        self.frame_bottom.pack(side="bottom", fill=BOTH, expand=YES)
        frame_left = FrameLeft(self.frame_bottom,user)  # 下方左边
        frame_left.pack(side="left", fill=Y)
        self.frame_right = Home(self.frame_bottom)  # 下方右边
        self.frame_right.pack(side="right", fill=BOTH, expand=YES)


class Home(Frame):  # 主页
    def __init__(self, master):
        Frame.__init__(self, master)
        # self.label = Label(self, text=time.strftime('%Y-%m-%d %H:%M:%S %A', time.localtime(time.time()))
        #                    , font=("Arial Black", 24))
        # self.label.after(1000, self.trickit)
        # self.label.pack(pady=20)
        self.im=Image.open("fj.jpg")
        self.img=ImageTk.PhotoImage(self.im)
        self.label = Label(self,image=self.img).pack(pady=20)

    # def trickit(self):
    #     currentTime = time.strftime('%Y-%m-%d %H:%M:%S %A', time.localtime(time.time()))
    #     self.label.config(text=currentTime)
    #     self.update()
    #     self.label.after(1000, self.trickit)


def go_home(win):  # 返回主页
    win.frame_right.destroy()
    win.frame_right = Home(Main.flag.frame_bottom)
    win.frame_right.pack(side="right", fill=BOTH, expand=YES)


def personal_data(window,userName):  # 查询个人信息
    window.frame_right.destroy()
    window.frame_right = Frame(Main.flag.frame_bottom)
    window.frame_right.pack(side="right", fill=BOTH, expand=YES)
    frame_top = Frame(window.frame_right)
    frame_top.pack(side='top', fill=BOTH)
    frame_bottom = Frame(window.frame_right)
    frame_bottom.pack(side='bottom', fill=BOTH, expand=YES)
    scrollbar = Scrollbar(frame_bottom)
    scrollbar.pack(side='right', fill=Y)
    tree = ttk.Treeview(frame_bottom, columns=list(range(5)), show='headings', yscrollcommand=scrollbar.set)
    column_name = ["顾客编号", "姓名", "性别", "联系电话","积分"]
    for i in range(5):
        tree.column(str(i), anchor='w')
        tree.heading(str(i), text=column_name[i], anchor='w')
    tree.pack(fill=BOTH, expand=YES)
    for row in get_userData("userName = '{}'".format(userName)):
        tree.insert('', 'end', values=row)
    scrollbar.config(command=tree.yview)

    
    popup_menu = Menu(frame_bottom, tearoff=0)

    def is_select():  # 判断Treeview中是否有行被选中
        flag = False
        for elem in tree.selection():
            flag = True
        return flag

    def show_all():
        [tree.delete(item) for item in tree.get_children()]
        for row in get_userData("userName = '{}'".format(userName)):
            tree.insert('', 'end', values=row)

    def alter():  # 修改顾客信息
        if is_select():
            for elem in tree.selection():
                win = Toplevel()
                win.grab_set()  # 模态
                win.focus()
                center(win, 300, 400)
                xb = ttk.Combobox(win, value=['M','F'], state='readonly')
                labels = [Label(win, text='修改个人信息', fg='blue', font=('楷体', 14)),
                          Label(win, text='顾客编号：' + tree.item(elem, 'values')[0]),
                          Label(win, text="姓名"), Entry(win),
                          Label(win, text="性别"), xb,
                          Label(win, text="密码"), Entry(win),
                          Label(win, text="联系电话"), Entry(win)]
                for l in labels:
                    l.pack()

                def confirm():  # 确认添加事件
                    sql = "update customerUser set realName='%s', sex='%s', password='%s', phone='%s', vip = 1.0  where userId='%s'"
                    data = []
                    for text in labels[3::2]:  # 切片 获取Entry， 再将其上面的文本内容添加到data里
                        data.append(text.get())
                    data.append(tree.item(elem, 'values')[0])
                    try:
                        execute_sql(sql % tuple(data))  # 字符串格式化
                        tkinter.messagebox.showinfo("SUCCEED", "修改成功！")
                        show_all()
                        win.destroy()
                    except pymysql.Error:
                        tkinter.messagebox.showerror("ERROR", "输入有误！")
                        win.focus()

                Button(win, text='确认修改', command=lambda: confirm()).pack()
        else:
            tkinter.messagebox.showerror("ERROR", "未选择顾客！")

    def delete():  # 删除顾客信息
        if is_select():
            if tkinter.messagebox.askokcancel('警告', '确认注销账号吗，您的所有积分将会丢失？'):
                for elem in tree.selection():
                    try:
                        execute_sql("delete from customerUser where userId='{}'".format(tree.item(elem, 'values')[0]))
                        tkinter.messagebox.showinfo('Succeed', '注销成功！')
                        tkinter.messagebox.showinfo('即将退出', '期待您的再次使用')
                        sys.exit(0)
                    except pymysql.Error:
                        tkinter.messagebox.showerror('Failed', '删除失败!')
        else:
            tkinter.messagebox.showerror('ERROR', '未选择！')

    def popup(event):  # 弹出右键菜单
        popup_menu.post(event.x_root, event.y_root)
    if VIPorNOT(userName):
        popup_menu.add_command(label='修改信息', command=lambda: alter())
    else:
        popup_menu.add_command(label='注册会员', command=lambda: alter())
    popup_menu.add_separator()
    popup_menu.add_command(label='注销账号', command=lambda: delete())
    tree.bind("<Button-3>", popup)


def personal_notice(window,userName):  # 查看个人消息
    userId = get_userId(userName)
    window.frame_right.destroy()
    window.frame_right = Frame(Main.flag.frame_bottom)
    window.frame_right.pack(side="right", fill=BOTH, expand=YES)
    frame_top = Frame(window.frame_right)
    frame_top.pack(side='top', fill=BOTH)
    frame_bottom = Frame(window.frame_right)
    frame_bottom.pack(side='bottom', fill=BOTH, expand=YES)
    scrollbar = Scrollbar(frame_bottom)
    scrollbar.pack(side='right', fill=Y)
    tree = ttk.Treeview(frame_bottom, columns=list(range(3)), show='headings', yscrollcommand=scrollbar.set)
    column_name = ["公告编号", "航班编号", "公告内容"]
    for i in range(3):
        tree.column(str(i), anchor='w')
        tree.heading(str(i), text=column_name[i], anchor='w')
    tree.pack(fill=BOTH, expand=YES)
    for row in get_board(userId):
        tree.insert('', 'end', values=row)
    scrollbar.config(command=tree.yview)

    
    popup_menu = Menu(frame_bottom, tearoff=0)


def personal_flight(window,userName=''):  # 查询， 统计航班信息
    window.frame_right.destroy()
    window.frame_right = Frame(Main.flag.frame_bottom)
    window.frame_right.pack(side="right", fill=BOTH, expand=YES)
    frame_top = Frame(window.frame_right)
    frame_top.pack(side='top', fill=BOTH)
    frame_bottom = Frame(window.frame_right)
    frame_bottom.pack(side='bottom', fill=BOTH, expand=YES)

    scrollbar = Scrollbar(frame_bottom)
    scrollbar.pack(side='right', fill=Y)
    tree = ttk.Treeview(frame_bottom, columns=list(range(8)), show='headings', yscrollcommand=scrollbar.set)
    column_name = ["编号", "飞机机型", "出发地","目的地","票价","航空公司", "出发时间", "剩余票量"]

    for i in range(8):
        tree.column(str(i), width=100, anchor='w')
        tree.heading(str(i), text=column_name[i], anchor='w')
    tree.column('3', width=120)
    tree.pack(fill=BOTH, expand=YES)
    for row in get_flightData(1):
        tree.insert('', 'end', values=row)
    scrollbar.config(command=tree.yview)

    def show_all():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData(1):
            tree.insert('', 'end', values=new_row)

    def no_search(event):
        [tree.delete(item) for item in tree.get_children()]
        for row_search in get_flightData(" flightId = '{}'".format(label_list[1].get())):
            tree.insert('', 'end', values=row_search)

    def show_no():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData(" leftTicket>0"):
            tree.insert('', 'end', values=new_row)

    def show_yes():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData(" leftTicket=0"):
            tree.insert('', 'end', values=new_row)

    def show_d(event):
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData(" departure='{}'".format(get_airportId1(cmb_d.get()))):
            tree.insert('', 'end', values=new_row)

    def show_t(event):
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData(" terminal='{}'".format(get_airportId1(cmb_t.get()))):
            tree.insert('', 'end', values=new_row)

    popup_menu = Menu(frame_bottom, tearoff=0)

    def is_select():  # 判断Treeview中是否有行被选中
        flag = False
        for elem in tree.selection():
            flag = True
        return flag

    def buy():  # 购买机票
        if is_select():
            for elem in tree.selection():
                leftTicket = get_leftTicket(tree.item(elem, 'values')[0])-1
                if leftTicket<0:
                    tkinter.messagebox.showinfo("提示", "余票不足，无法购买！")
                    return 
                win = Toplevel()
                win.grab_set()  # 模态
                win.focus()
                center(win, 300, 400)
                seat = ttk.Combobox(win, value=get_seat(tree.item(elem, 'values')[0]), state='readonly')
                discount = get_discount(userName)
                d_price = int(float(tree.item(elem, 'values')[4]) * discount)
                labels = [Label(win, text='购买机票', fg='blue', font=('楷体', 14)),
                          Label(win, text='航班编号：' + tree.item(elem, 'values')[0]),
                          Label(win, text='优惠价格：' + str(d_price)),
                          Label(win, text="乘客姓名"), Entry(win),
                          Label(win, text="乘客手机号"), Entry(win),
                          Label(win, text="选择座位"), seat]
                for l in labels:
                    l.pack()


                def confirm():  # 确认添加事件
                    string_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
                    new_points = get_points(userName)+int(tree.item(elem, 'values')[4])
                    sql1= "insert into ticket values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                    sql2= "update flight set leftTicket = {} where flightId = {}".format(leftTicket,tree.item(elem, 'values')[0])
                    sql3= "update customerUser set point = {} where userName = '{}'".format(new_points,userName)
                    data = [string_time,get_userId(userName),tree.item(elem, 'values')[0],get_companyId(tree.item(elem, 'values')[5]), labels[8].get(),labels[4].get(),labels[6].get(), d_price,time.strftime("%Y/%m/%d", time.localtime())]
                    try:
                        execute_sql(sql1 % tuple(data))  # 添加购买记录
                        execute_sql(sql2)               # 更新余票数额
                        execute_sql(sql3)               # 更新用户积分
                        tkinter.messagebox.showinfo("SUCCEED", "购买成功！")
                        show_all()
                        win.destroy()
                    except pymysql.Error:
                        tkinter.messagebox.showerror("ERROR", "输入有误！")
                        win.focus()
                Button(win, text='确认购买', command=lambda: confirm()).pack()
        else:
            tkinter.messagebox.showerror("ERROR", "未选择航班！")

    def popup(event):  # 弹出右键菜单
        popup_menu.post(event.x_root, event.y_root)

    def price_sort():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData(" 1 order by ticketMoney"):
            tree.insert('', 'end', values=new_row)

    def time_sort():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData(" 1 order by leaveTime"):
            tree.insert('', 'end', values=new_row)

    tree.heading("0", text="航班编号", command=lambda: show_all())  # 点击表头排序
    tree.heading("4", text="票价", command=lambda: price_sort())  # 点击表头排序
    tree.heading("6", text="出发时间", command=lambda: time_sort())  # 点击表头排序

    popup_menu.add_command(label='购买', command=lambda: buy())


    Label(frame_top, text='查询售票 ：', font=('楷体', 18), fg='blue').pack(side='left', fill=BOTH, expand=YES)
    Label(frame_top, text='出发地').pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    cmb_d = ttk.Combobox(frame_top, value=get_airportName('all'), state='readonly', width=5)   
    cmb_d.pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    cmb_d.bind("<<ComboboxSelected>>", show_d)

    Label(frame_top, text='目的地').pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    cmb_t = ttk.Combobox(frame_top, value=get_airportName('all'), state='readonly', width=5)   
    cmb_t.pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    cmb_t.bind("<<ComboboxSelected>>", show_t)

    Label(frame_top, text='价格区间').pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    left = Entry(frame_top, width=8)
    left.pack(side="left", fill=X, expand=YES, padx=0, pady=2)
    Label(frame_top, text='至').pack(side="left", fill=X, expand=YES, padx=0, pady=2)
    right = Entry(frame_top, width=8)
    right.pack(side="left", fill=X, expand=YES, padx=0, pady=2)

    def range_search(event):
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData(" ticketMoney>={} and ticketMoney<={};".format(left.get(), right.get())):
            tree.insert('', 'end', values=new_row)
    right.bind('<Key-Return>', range_search)
    button_no = Button(frame_top, text='未售空', font=('楷体', 12), command=show_no)
    button_yes = Button(frame_top, text='已售空', font=('楷体', 12), command=show_yes)
    button = Button(frame_top, text='显示所有', font=('楷体', 12), command=show_all)
    button_no.pack(side='left', fill=X, expand=YES, padx=3, pady=5)
    button_yes.pack(side='left', fill=X, expand=YES, padx=3, pady=5)
    button.pack(side='left', fill=X, expand=YES, padx=3, pady=5)
    tree.bind("<Button-3>", popup)


def personal_ticket(window,username):  # 查询个人票务信息
    window.frame_right.destroy()
    window.frame_right = Frame(Main.flag.frame_bottom)
    window.frame_right.pack(side="right", fill=BOTH, expand=YES)
    frame_top = Frame(window.frame_right)
    frame_top.pack(side='top', fill=BOTH)
    frame_bottom = Frame(window.frame_right)
    frame_bottom.pack(side='bottom', fill=BOTH, expand=YES)
    Label(frame_top, text='查询个人票务信息：', font=('楷体', 18), fg='blue').pack(side='left', fill=BOTH, expand=YES)
    label_list = [Label(frame_top, text='顾客姓名'), Entry(frame_top, width=10),
                  Label(frame_top, text='航班编号'), Entry(frame_top, width=10),
                  Label(frame_top, text='选择所属公司')]
    for label in label_list:
        label.pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    scrollbar = Scrollbar(frame_bottom)
    scrollbar.pack(side='right', fill=Y)
    tree = ttk.Treeview(frame_bottom, columns=list(range(9)), show='headings', yscrollcommand=scrollbar.set)
    column_name = ["订单号", "用户ID", "航班ID", "航空公司", "座位号", "乘客姓名",
                   "电话号码", "售票价格","销售日期"]
    for i in range(9):
        tree.column(str(i), width=50, anchor='w')
        tree.heading(str(i), text=column_name[i], anchor='w')
    tree.column('6', width=100)
    tree.column('5', width=80)
    tree.column('8', width=120)
    tree.column('7', width=80)
    tree.pack(fill=BOTH, expand=YES)
    user_id = get_userId(username)
    for row in get_ticketData(" userId = '{}'".format(user_id)):
        tree.insert('', 'end', values=row)
    scrollbar.config(command=tree.yview)

    def show_all(): # 显示所有销售信息
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_ticketData(' userId = {}'.format(user_id)):
            tree.insert('', 'end', values=new_row)

    def cname_search(event):  # 按顾客姓名查找
        [tree.delete(item) for item in tree.get_children()]
        for row_search in get_ticketData(" userId = {} and passagerName like '%{}%'".format(user_id,label_list[1].get())):
            tree.insert('', 'end', values=row_search)

    def pno_search(event):  # 按飞机编号查找
        [tree.delete(item) for item in tree.get_children()]
        for row_search in get_ticketData(" flightId = {} and  userId = {}".format(label_list[3].get(),user_id)):
            tree.insert('', 'end', values=row_search)

    popup_menu = Menu(frame_bottom, tearoff=0)

    def is_select():  # 判断Treeview中是否有行被选中
        flag = False
        for elem in tree.selection():
            flag = True
        return flag

    def alter():  # 修改销售信息
        if is_select():
            for elem in tree.selection():
                win = Toplevel()
                win.grab_set()  # 模态
                win.focus()
                center(win, 300, 300)
                labels = [Label(win, text='修改销售信息', fg='blue', font=('楷体', 14)),
                          Label(win, text='订单编号：' + tree.item(elem, 'values')[0]),
                          Label(win, text="乘客姓名"), Entry(win),
                          Label(win, text="手机号码"), Entry(win)]
                for l in labels:
                    l.pack()
                def confirm():
                    sql_update = "update ticket set passagerName='%s', passagerPhone='%s' where ticketId= '%s'"
                    data = (labels[3].get(), labels[5].get(), tree.item(elem, 'values')[0])
                    try:
                        execute_sql(sql_update % data)
                        tkinter.messagebox.showinfo("SUCCEED", "修改成功")
                        win.destroy()
                        show_all()
                    except pymysql.Error:
                        tkinter.messagebox.showerror("Failed", "修改失败")
                        win.focus()

                Button(win, text='确认修改', command=lambda: confirm()).pack(pady=20)
        else:
            tkinter.messagebox.showerror("ERROR", "未选择机票信息！")

    def delete():  # 删除机票信息
        if is_select():
            if tkinter.messagebox.askokcancel('警告', '确认退订该机票吗？'):
                for elem in tree.selection():
                    try:
                        new_points = get_points(username)-int(tree.item(elem, 'values')[7])
                        sql= "update customerUser set point = {} where userName = '{}'".format(new_points,username)
                        execute_sql(sql)
                        execute_sql("delete from ticket where ticketId='{}'".format(tree.item(elem, 'values')[0]))
                        tkinter.messagebox.showinfo('Succeed', '删除成功！')
                        show_all()
                    except pymysql.Error:
                        tkinter.messagebox.showerror('Failed', '删除失败!')
        else:
            tkinter.messagebox.showerror('ERROR', '未选择机票信息！')

    def popup(event):  # 弹出右键菜单
        popup_menu.post(event.x_root, event.y_root)

    def price_sort():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_ticketData("1 order by paidMoney"):
            tree.insert('', 'end', values=new_row)

    def date_sort():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_ticketData("1 order by paidTime"):
            tree.insert('', 'end', values=new_row)

    tree.heading("7", text="单价", command=lambda: price_sort())  # 点击表头排序
    tree.heading("8", text="销售日期", command=lambda: date_sort())  # 点击表头排序

    popup_menu.add_command(label='修改乘客', command=lambda: alter())
    popup_menu.add_separator()
    popup_menu.add_command(label='退票', command=lambda: delete())

    label_list[1].bind('<Key-Return>', cname_search)  # 回车 按顾客姓名查询
    label_list[3].bind('<Key-Return>', pno_search)  # 回车 按宠物编号查询

    def show(event):
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_ticketData(" ticket.companyId ={}".format(cmb.get())):
            tree.insert('', 'end', values=new_row)

    cmb = ttk.Combobox(frame_top, value=get_companyId('ticket'), state='readonly', width=5)
    cmb.pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    cmb.bind("<<ComboboxSelected>>", show)

    button = Button(frame_top, text='显示所有', font=('楷体', 14), command=show_all)
    button.pack(side='left', fill=X, expand=YES, padx=3, pady=5)
    tree.bind("<Button-3>", popup)


def search_client(window):  # 查询， 统计客户信息
    window.frame_right.destroy()
    window.frame_right = Frame(Main.flag.frame_bottom)
    window.frame_right.pack(side="right", fill=BOTH, expand=YES)
    frame_top = Frame(window.frame_right)
    frame_top.pack(side='top', fill=BOTH)
    frame_bottom = Frame(window.frame_right)
    frame_bottom.pack(side='bottom', fill=BOTH, expand=YES)
    Label(frame_top, text='查询统计顾客信息：', font=('楷体', 18), fg='blue').pack(side='left', fill=BOTH, expand=YES)
    label_list = [Label(frame_top, text='顾客编号:'), Entry(frame_top), Label(frame_top, text='顾客姓名:'),
                  Entry(frame_top)]
    for label in label_list:
        label.pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    scrollbar = Scrollbar(frame_bottom)
    scrollbar.pack(side='right', fill=Y)
    tree = ttk.Treeview(frame_bottom, columns=list(range(5)), show='headings', yscrollcommand=scrollbar.set)
    column_name = ["顾客编号", "姓名", "性别", "联系电话","积分"]
    for i in range(5):
        tree.column(str(i), anchor='w')
        tree.heading(str(i), text=column_name[i], anchor='w')
    tree.pack(fill=BOTH, expand=YES)
    for row in get_userData('vip = 1'):
        tree.insert('', 'end', values=row)
    scrollbar.config(command=tree.yview)

    def show_all():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_userData(1):
            tree.insert('', 'end', values=new_row)

    def no_search(event):
        [tree.delete(item) for item in tree.get_children()]
        sql = "SELECT * FROM psms.client where cno={}"
        for row_search in get_userData('userId = {}'.format(label_list[1].get())):
            tree.insert('', 'end', values=row_search)

    def name_search(event):
        [tree.delete(item) for item in tree.get_children()]
        for row_search in get_userData(" realName like '%{}%'".format(label_list[3].get())):
            tree.insert('', 'end', values=row_search)

    popup_menu = Menu(frame_bottom, tearoff=0)

    def is_select():  # 判断Treeview中是否有行被选中
        flag = False
        for elem in tree.selection():
            flag = True
        return flag

    def alter():  # 修改顾客信息
        if is_select():
            for elem in tree.selection():
                win = Toplevel()
                win.grab_set()  # 模态
                win.focus()
                center(win, 300, 400)
                labels = [Label(win, text='修改顾客信息', fg='blue', font=('楷体', 14)),
                          Label(win, text='顾客编号：' + tree.item(elem, 'values')[0]),
                          Label(win, text="姓名"), Entry(win),
                          Label(win, text="性别"), Entry(win),
                          Label(win, text="积分"), Entry(win),
                          Label(win, text="联系电话"), Entry(win)]
                for l in labels:
                    l.pack()

                def confirm():  # 确认添加事件
                    sql = "update customerUser set realName='%s', sex='%s', point='%s', phone='%s' where userId='%s'"
                    data = []
                    for text in labels[3::2]:  # 切片 获取Entry， 再将其上面的文本内容添加到data里
                        data.append(text.get())
                    data.append(tree.item(elem, 'values')[0])
                    try:
                        execute_sql(sql % tuple(data))  # 字符串格式化
                        tkinter.messagebox.showinfo("SUCCEED", "修改成功！")
                        show_all()
                        win.destroy()
                    except pymysql.Error:
                        tkinter.messagebox.showerror("ERROR", "输入有误！")
                        win.focus()

                Button(win, text='确认修改', command=lambda: confirm()).pack()
        else:
            tkinter.messagebox.showerror("ERROR", "未选择顾客！")

    def delete():  # 删除顾客信息
        if is_select():
            if tkinter.messagebox.askokcancel('警告', '确认删除该顾客信息吗？'):
                for elem in tree.selection():
                    try:
                        execute_sql("delete from customerUser where userId='{}'".format(tree.item(elem, 'values')[0]))
                        tkinter.messagebox.showinfo('Succeed', '删除成功！')
                        show_all()
                    except pymysql.Error:
                        tkinter.messagebox.showerror('Failed', '删除失败!')
        else:
            tkinter.messagebox.showerror('ERROR', '未选择顾客！')

    def popup(event):  # 弹出右键菜单
        popup_menu.post(event.x_root, event.y_root)
    popup_menu.add_command(label='修改', command=lambda: alter())
    popup_menu.add_separator()
    popup_menu.add_command(label='删除', command=lambda: delete())
    label_list[1].bind('<Key-Return>', no_search)
    label_list[3].bind('<Key-Return>', name_search)
    button = Button(frame_top, text='显示所有', font=('楷体', 14), command=show_all)
    button.pack(side='left', fill=X, expand=YES, padx=3, pady=5)
    tree.bind("<Button-3>", popup)


def search_flight(window,userName='',usertype = 0):  # 查询， 统计航班信息
    window.frame_right.destroy()
    window.frame_right = Frame(Main.flag.frame_bottom)
    window.frame_right.pack(side="right", fill=BOTH, expand=YES)
    frame_top = Frame(window.frame_right)
    frame_top.pack(side='top', fill=BOTH)
    frame_bottom = Frame(window.frame_right)
    frame_bottom.pack(side='bottom', fill=BOTH, expand=YES)
    Label(frame_top, text='查询售票 ：', font=('楷体', 18), fg='blue').pack(side='left', fill=BOTH, expand=YES)
    label_list = [Label(frame_top, text='机票编号'), Entry(frame_top, width=7), Label(frame_top, text='选择飞机类型')]
    for label in label_list:
        label.pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    scrollbar = Scrollbar(frame_bottom)
    scrollbar.pack(side='right', fill=Y)
    tree = ttk.Treeview(frame_bottom, columns=list(range(8)), show='headings', yscrollcommand=scrollbar.set)
    column_name = ["编号", "飞机机型", "出发地","目的地","票价","航空公司", "出发时间", "剩余票量"]

    for i in range(8):
        tree.column(str(i), width=100, anchor='w')
        tree.heading(str(i), text=column_name[i], anchor='w')
    tree.column('3', width=120)
    tree.pack(fill=BOTH, expand=YES)
    for row in get_flightData(1):
        tree.insert('', 'end', values=row)
    scrollbar.config(command=tree.yview)

    def show_all():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData(1):
            tree.insert('', 'end', values=new_row)

    def no_search(event):
        [tree.delete(item) for item in tree.get_children()]
        for row_search in get_flightData(" flightId = '{}'".format(label_list[1].get())):
            tree.insert('', 'end', values=row_search)

    def show_no():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData(" leftTicket>0"):
            tree.insert('', 'end', values=new_row)

    def show_yes():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData(" leftTicket=0"):
            tree.insert('', 'end', values=new_row)

    popup_menu = Menu(frame_bottom, tearoff=0)

    def is_select():  # 判断Treeview中是否有行被选中
        flag = False
        for elem in tree.selection():
            flag = True
        return flag

    def buy():  # 购买机票
        if is_select():
            for elem in tree.selection():
                leftTicket = get_leftTicket(tree.item(elem, 'values')[0])-1
                if leftTicket<0:
                    tkinter.messagebox.showinfo("提示", "余票不足，无法购买！")
                    return 
                win = Toplevel()
                win.grab_set()  # 模态
                win.focus()
                center(win, 300, 400)
                seat = ttk.Combobox(win, value=get_seat(tree.item(elem, 'values')[0]), state='readonly')
                discount = get_discount(userName)
                d_price = int(float(tree.item(elem, 'values')[4]) * discount)
                labels = [Label(win, text='购买机票', fg='blue', font=('楷体', 14)),
                          Label(win, text='航班编号：' + tree.item(elem, 'values')[0]),
                          Label(win, text='优惠价格：' + str(d_price)),
                          Label(win, text="乘客姓名"), Entry(win),
                          Label(win, text="乘客手机号"), Entry(win),
                          Label(win, text="选择座位"), seat]
                for l in labels:
                    l.pack()


                def confirm():  # 确认添加事件
                    string_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
                    new_points = get_points(userName)+int(tree.item(elem, 'values')[4])
                    sql1= "insert into ticket values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                    sql2= "update flight set leftTicket = {} where flightId = {}".format(leftTicket,tree.item(elem, 'values')[0])
                    sql3= "update customerUser set point = {} where userName = '{}'".format(new_points,userName)
                    data = [string_time,get_userId(userName),tree.item(elem, 'values')[0],get_companyId(tree.item(elem, 'values')[5]), labels[8].get(),labels[4].get(),labels[6].get(), d_price,time.strftime("%Y/%m/%d", time.localtime())]
                    try:
                        execute_sql(sql1 % tuple(data))  # 添加购买记录
                        execute_sql(sql2)               # 更新余票数额
                        execute_sql(sql3)               # 更新用户积分
                        tkinter.messagebox.showinfo("SUCCEED", "购买成功！")
                        show_all()
                        win.destroy()
                    except pymysql.Error:
                        tkinter.messagebox.showerror("ERROR", "输入有误！")
                        win.focus()
                Button(win, text='确认购买', command=lambda: confirm()).pack()
        else:
            tkinter.messagebox.showerror("ERROR", "未选择航班！")

    def alter():  # 修改航班信息
        if is_select():
            for elem in tree.selection():
                win = Toplevel()
                win.grab_set()  # 模态
                win.focus()
                center(win, 300, 400)
                labels = [Label(win, text='修改航班信息', fg='blue', font=('楷体', 14)),
                          Label(win, text='航班编号：' + tree.item(elem, 'values')[0]),
                          Label(win, text="出发时间"), Entry(win),
                          Label(win, text="票价"), Entry(win),
                          Label(win, text="出发地"), Entry(win),
                          Label(win, text="目的地"), Entry(win),
                          Label(win, text="余票数量"), Entry(win)]
                for l in labels:
                    l.pack()

                def confirm():  # 确认添加事件
                    sql = "update flight set plane='%s',leaveTime=%s, ticketMoney=%s, departure'%s', terminal='%s' where flightId='%s'"
                    data = []
                    for text in labels[3::2]:  # 切片 获取Entry， 再将其上面的文本内容添加到data里
                        data.append(text.get())
                    data.append(tree.item(elem, 'values')[0])
                    try:
                        execute_sql(sql % tuple(data))  # 字符串格式化
                        tkinter.messagebox.showinfo("SUCCEED", "修改成功！")
                        show_all()
                        win.destroy()
                    except pymysql.Error:
                        tkinter.messagebox.showerror("ERROR", "输入有误！")
                        win.focus()
                Button(win, text='确认修改', command=lambda: confirm()).pack()
        else:
            tkinter.messagebox.showerror("ERROR", "未选择航班！")

    def delete():  # 删除航班信息
        if is_select():
            if tkinter.messagebox.askokcancel('警告', '确认删除航班信息吗？'):
                for elem in tree.selection():
                    try:
                        execute_sql("delete from flight where flightId='{}'".format(tree.item(elem, 'values')[0]))
                        tkinter.messagebox.showinfo('Succeed', '删除成功！')
                        show_all()
                    except pymysql.Error:
                        tkinter.messagebox.showerror('Failed', '删除失败!')
        else:
            tkinter.messagebox.showerror('ERROR', '未选择航班！')

    def popup(event):  # 弹出右键菜单
        popup_menu.post(event.x_root, event.y_root)

    def price_sort():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData(" 1 order by ticketMoney"):
            tree.insert('', 'end', values=new_row)

    def time_sort():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData(" 1 order by leaveTime"):
            tree.insert('', 'end', values=new_row)

    tree.heading("0", text="航班编号", command=lambda: show_all())  # 点击表头排序
    tree.heading("4", text="票价", command=lambda: price_sort())  # 点击表头排序
    tree.heading("6", text="出发时间", command=lambda: time_sort())  # 点击表头排序

    if usertype == 1:
        popup_menu.add_command(label='购买', command=lambda: buy())
    else:
        popup_menu.add_command(label='修改', command=lambda: alter())
        popup_menu.add_separator()
        popup_menu.add_command(label='删除', command=lambda: delete())

    label_list[1].bind('<Key-Return>', no_search)  # 回车 按航班编号查询

    def show(event):
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData(" plane='{}'".format(cmb.get())):
            tree.insert('', 'end', values=new_row)

    type_p = []
    for result in execute_sql("select distinct plane from flight"):
        type_p.append(result)
    cmb = ttk.Combobox(frame_top, value=type_p, state='readonly', width=5)   # 添加选择宠物类型的下拉列表
    cmb.pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    cmb.bind("<<ComboboxSelected>>", show)
    Label(frame_top, text='价格区间').pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    left = Entry(frame_top, width=8)
    left.pack(side="left", fill=X, expand=YES, padx=0, pady=2)
    Label(frame_top, text='至').pack(side="left", fill=X, expand=YES, padx=0, pady=2)
    right = Entry(frame_top, width=8)
    right.pack(side="left", fill=X, expand=YES, padx=0, pady=2)

    def range_search(event):
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData(" ticketMoney>={} and ticketMoney<={};".format(left.get(), right.get())):
            tree.insert('', 'end', values=new_row)
    right.bind('<Key-Return>', range_search)
    button_no = Button(frame_top, text='未售空', font=('楷体', 12), command=show_no)
    button_yes = Button(frame_top, text='已售空', font=('楷体', 12), command=show_yes)
    button = Button(frame_top, text='显示所有', font=('楷体', 12), command=show_all)
    button_no.pack(side='left', fill=X, expand=YES, padx=3, pady=5)
    button_yes.pack(side='left', fill=X, expand=YES, padx=3, pady=5)
    button.pack(side='left', fill=X, expand=YES, padx=3, pady=5)
    tree.bind("<Button-3>", popup)


def airport_flight(window,userName=''):  # 查询机场航班信息
    window.frame_right.destroy()
    window.frame_right = Frame(Main.flag.frame_bottom)
    window.frame_right.pack(side="right", fill=BOTH, expand=YES)
    frame_top = Frame(window.frame_right)
    frame_top.pack(side='top', fill=BOTH)
    frame_bottom = Frame(window.frame_right)
    frame_bottom.pack(side='bottom', fill=BOTH, expand=YES)
    Label(frame_top, text='查询售票 ：', font=('楷体', 18), fg='blue').pack(side='left', fill=BOTH, expand=YES)
    label_list = [Label(frame_top, text='机票编号'), Entry(frame_top, width=7), Label(frame_top, text='选择飞机类型')]
    for label in label_list:
        label.pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    scrollbar = Scrollbar(frame_bottom)
    scrollbar.pack(side='right', fill=Y)
    tree = ttk.Treeview(frame_bottom, columns=list(range(8)), show='headings', yscrollcommand=scrollbar.set)
    column_name = ["编号", "飞机机型", "出发地","目的地","票价","航空公司", "出发时间", "剩余票量"]
    airportId = get_airportId(userName)
    for i in range(8):
        tree.column(str(i), width=100, anchor='w')
        tree.heading(str(i), text=column_name[i], anchor='w')
    tree.column('3', width=120)
    tree.pack(fill=BOTH, expand=YES)
    for row in get_airport_flightData(airportId,1):
        tree.insert('', 'end', values=row)
    scrollbar.config(command=tree.yview)

    def show_all():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_airport_flightData(airportId,1):
            tree.insert('', 'end', values=new_row)

    def no_search(event):
        [tree.delete(item) for item in tree.get_children()]
        for row_search in get_airport_flightData(airportId," flightId = '{}'".format(label_list[1].get())):
            tree.insert('', 'end', values=row_search)

    def show_no():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_airport_flightData(airportId," leftTicket>0"):
            tree.insert('', 'end', values=new_row)

    def show_yes():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_airport_flightData(airportId," leftTicket=0"):
            tree.insert('', 'end', values=new_row)

    popup_menu = Menu(frame_bottom, tearoff=0)

    def is_select():  # 判断Treeview中是否有行被选中
        flag = False
        for elem in tree.selection():
            flag = True
        return flag

    def alter():  # 修改航班信息
        if is_select():
            for elem in tree.selection():
                win = Toplevel()
                win.grab_set()  # 模态
                win.focus()
                center(win, 300, 400)
                c = tkinter.IntVar()
                c.set(1)
                check = tkinter.Checkbutton(win,text='通知已购票用户',variable = c,onvalue =1,offvalue=2)
                labels = [Label(win, text='修改航班信息', fg='blue', font=('楷体', 14)),
                          Label(win, text='航班编号：' + tree.item(elem, 'values')[0]),
                          Label(win, text="出发时间"), Entry(win),
                          Label(win, text="票价"), Entry(win),
                          Label(win, text="出发地"), Entry(win),
                          Label(win, text="目的地"), Entry(win),
                          Label(win, text="余票数量"), Entry(win)]
                for l in labels:
                    l.pack()
                check.pack()

                def confirm():  # 确认添加事件
                    sql = "update flight set leaveTime='%s', ticketMoney=%s, departure = '%s', terminal='%s',leftTicket = '%s' where flightId='%s'"

                    data = []
                    for text in labels[3::2]:  # 切片 获取Entry， 再将其上面的文本内容添加到data里
                        data.append(text.get())
                    data.append(tree.item(elem, 'values')[0])
                    try:
                        if  c.get() == 1:
                            add_board(tree.item(elem, 'values')[0],labels[3].get())   #添加公告，提示所有预定了此航班的乘客
                        execute_sql(sql % tuple(data))  # 字符串格式化
                        tkinter.messagebox.showinfo("SUCCEED", "修改成功！")
                        show_all()
                        win.destroy()
                    except pymysql.Error:
                        tkinter.messagebox.showerror("ERROR", "输入有误！")
                        win.focus()
                Button(win, text='确认修改', command=lambda: confirm()).pack()
        else:
            tkinter.messagebox.showerror("ERROR", "未选择航班！")

    def delete():  # 删除航班信息
        if is_select():
            if tkinter.messagebox.askokcancel('警告', '确认删除航班信息吗？'):
                for elem in tree.selection():
                    try:
                        execute_sql("delete from flight where flightId='{}'".format(tree.item(elem, 'values')[0]))
                        tkinter.messagebox.showinfo('Succeed', '删除成功！')
                        show_all()
                    except pymysql.Error:
                        tkinter.messagebox.showerror('Failed', '删除失败!')
        else:
            tkinter.messagebox.showerror('ERROR', '未选择航班！')

    def popup(event):  # 弹出右键菜单
        popup_menu.post(event.x_root, event.y_root)

    def price_sort():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_airport_flightData(airportId," 1 order by ticketMoney"):
            tree.insert('', 'end', values=new_row)

    def time_sort():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_airport_flightData(airportId," 1 order by leaveTime"):
            tree.insert('', 'end', values=new_row)

    tree.heading("0", text="航班编号", command=lambda: show_all())  # 点击表头排序
    tree.heading("4", text="票价", command=lambda: price_sort())  # 点击表头排序
    tree.heading("6", text="出发时间", command=lambda: time_sort())  # 点击表头排序

    popup_menu.add_command(label='修改', command=lambda: alter())
    popup_menu.add_separator()
    popup_menu.add_command(label='删除', command=lambda: delete())

    label_list[1].bind('<Key-Return>', no_search)  # 回车 按航班编号查询

    def show(event):
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_airport_flightData(airportId," plane='{}'".format(cmb.get())):
            tree.insert('', 'end', values=new_row)

    type_p = []
    for result in execute_sql("select distinct plane from flight"):
        type_p.append(result)
    cmb = ttk.Combobox(frame_top, value=type_p, state='readonly', width=5)   # 添加选择宠物类型的下拉列表
    cmb.pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    cmb.bind("<<ComboboxSelected>>", show)
    Label(frame_top, text='价格区间').pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    left = Entry(frame_top, width=8)
    left.pack(side="left", fill=X, expand=YES, padx=0, pady=2)
    Label(frame_top, text='至').pack(side="left", fill=X, expand=YES, padx=0, pady=2)
    right = Entry(frame_top, width=8)
    right.pack(side="left", fill=X, expand=YES, padx=0, pady=2)

    def range_search(event):
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_airport_flightData(airportId," ticketMoney>={} and ticketMoney<={};".format(left.get(), right.get())):
            tree.insert('', 'end', values=new_row)
    right.bind('<Key-Return>', range_search)
    button_no = Button(frame_top, text='未售空', font=('楷体', 12), command=show_no)
    button_yes = Button(frame_top, text='已售空', font=('楷体', 12), command=show_yes)
    button = Button(frame_top, text='显示所有', font=('楷体', 12), command=show_all)
    button_no.pack(side='left', fill=X, expand=YES, padx=3, pady=5)
    button_yes.pack(side='left', fill=X, expand=YES, padx=3, pady=5)
    button.pack(side='left', fill=X, expand=YES, padx=3, pady=5)
    tree.bind("<Button-3>", popup)


def company_flight(window,userName=''):  # 查询公司航班信息
    window.frame_right.destroy()
    window.frame_right = Frame(Main.flag.frame_bottom)
    window.frame_right.pack(side="right", fill=BOTH, expand=YES)
    frame_top = Frame(window.frame_right)
    frame_top.pack(side='top', fill=BOTH)
    frame_bottom = Frame(window.frame_right)
    frame_bottom.pack(side='bottom', fill=BOTH, expand=YES)
    Label(frame_top, text='查询售票 ：', font=('楷体', 18), fg='blue').pack(side='left', fill=BOTH, expand=YES)
    label_list = [Label(frame_top, text='机票编号'), Entry(frame_top, width=7), Label(frame_top, text='选择飞机类型')]
    for label in label_list:
        label.pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    scrollbar = Scrollbar(frame_bottom)
    scrollbar.pack(side='right', fill=Y)
    tree = ttk.Treeview(frame_bottom, columns=list(range(8)), show='headings', yscrollcommand=scrollbar.set)
    column_name = ["编号", "飞机机型", "出发地","目的地","票价","航空公司", "出发时间", "剩余票量"]

    for i in range(8):
        tree.column(str(i), width=100, anchor='w')
        tree.heading(str(i), text=column_name[i], anchor='w')
    tree.column('3', width=120)
    tree.pack(fill=BOTH, expand=YES)
    companyId = get_companyId_by_user(userName)
    for row in get_flightData2(companyId,1):
        tree.insert('', 'end', values=row)
    scrollbar.config(command=tree.yview)

    def show_all():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData2(companyId,1):
            tree.insert('', 'end', values=new_row)

    def no_search(event):
        [tree.delete(item) for item in tree.get_children()]
        for row_search in get_flightData2(companyId," flightId = '{}'".format(label_list[1].get())):
            tree.insert('', 'end', values=row_search)

    def show_no():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData2(companyId," leftTicket>0"):
            tree.insert('', 'end', values=new_row)

    def show_yes():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData2(companyId," leftTicket=0"):
            tree.insert('', 'end', values=new_row)

    popup_menu = Menu(frame_bottom, tearoff=0)

    def is_select():  # 判断Treeview中是否有行被选中
        flag = False
        for elem in tree.selection():
            flag = True
        return flag

    def alter():  # 修改航班信息
        if is_select():
            for elem in tree.selection():
                win = Toplevel()
                win.grab_set()  # 模态
                win.focus()
                center(win, 300, 400)
                c = tkinter.IntVar()
                check = tkinter.Checkbutton(win,text='通知已购票用户',variable = c,onvalue =1,offvalue=2)
                labels = [Label(win, text='修改航班信息', fg='blue', font=('楷体', 14)),
                          Label(win, text='航班编号：' + tree.item(elem, 'values')[0]),
                          Label(win, text="出发时间"), Entry(win),
                          Label(win, text="票价"), Entry(win),
                          Label(win, text="出发地"), Entry(win),
                          Label(win, text="目的地"), Entry(win),
                          Label(win, text="余票数量"), Entry(win)]
                for l in labels:
                    l.pack()
                check.pack()
                def confirm():  # 确认添加事件
                    sql = "update flight set plane='%s',leaveTime=%s, ticketMoney=%s, departure='%s', terminal='%s' where flightId='%s'"
                    data = []
                    for text in labels[3::2]:  # 切片 获取Entry， 再将其上面的文本内容添加到data里
                        data.append(text.get())
                    data.append(tree.item(elem, 'values')[0])
                    try:
                        if  c.get() == 1:
                            add_board(tree.item(elem, 'values')[0],labels[3].get())   #添加公告，提示所有预定了此航班的乘客
                        execute_sql(sql % tuple(data))  # 字符串格式化
                        tkinter.messagebox.showinfo("SUCCEED", "修改成功！")
                        show_all()
                        win.destroy()
                    except pymysql.Error:
                        tkinter.messagebox.showerror("ERROR", "输入有误！")
                        win.focus()
                Button(win, text='确认修改', command=lambda: confirm()).pack()
        else:
            tkinter.messagebox.showerror("ERROR", "未选择航班！")

    def delete():  # 删除航班信息
        if is_select():
            if tkinter.messagebox.askokcancel('警告', '确认取消该航班吗？'):
                for elem in tree.selection():
                    try:
                        if is_saled(tree.item(elem, 'values')[0]):
                            tkinter.messagebox.showinfo('Failed', '目前有{}位客户预定了机票，请通知所有用户退订后再删除!'.format(is_saled(tree.item(elem, 'values')[0])))
                            return 
                        execute_sql("delete from flight where flightId='{}'".format(tree.item(elem, 'values')[0]))
                        tkinter.messagebox.showinfo('Succeed', '删除成功！')
                        show_all()
                    except pymysql.Error:
                        tkinter.messagebox.showerror('Failed', '删除失败!')
        else:
            tkinter.messagebox.showerror('ERROR', '未选择航班！')

    def popup(event):  # 弹出右键菜单
        popup_menu.post(event.x_root, event.y_root)

    def price_sort():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData2(companyId," 1 order by ticketMoney"):
            tree.insert('', 'end', values=new_row)

    def time_sort():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData2(companyId," 1 order by leaveTime"):
            tree.insert('', 'end', values=new_row)

    tree.heading("0", text="航班编号", command=lambda: show_all())  # 点击表头排序
    tree.heading("4", text="票价", command=lambda: price_sort())  # 点击表头排序
    tree.heading("6", text="出发时间", command=lambda: time_sort())  # 点击表头排序


    popup_menu.add_command(label='修改航班', command=lambda: alter())
    popup_menu.add_separator()
    popup_menu.add_command(label='取消航班', command=lambda: delete())

    label_list[1].bind('<Key-Return>', no_search)  # 回车 按航班编号查询

    def show(event):
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData2(companyId," plane='{}'".format(cmb.get())):
            tree.insert('', 'end', values=new_row)

    type_p = []
    for result in execute_sql("select distinct plane from flight"):
        type_p.append(result)
    cmb = ttk.Combobox(frame_top, value=type_p, state='readonly', width=5)   # 添加选择宠物类型的下拉列表
    cmb.pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    cmb.bind("<<ComboboxSelected>>", show)
    Label(frame_top, text='价格区间').pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    left = Entry(frame_top, width=8)
    left.pack(side="left", fill=X, expand=YES, padx=0, pady=2)
    Label(frame_top, text='至').pack(side="left", fill=X, expand=YES, padx=0, pady=2)
    right = Entry(frame_top, width=8)
    right.pack(side="left", fill=X, expand=YES, padx=0, pady=2)

    def range_search(event):
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_flightData2(companyId," ticketMoney>={} and ticketMoney<={};".format(left.get(), right.get())):
            tree.insert('', 'end', values=new_row)
    right.bind('<Key-Return>', range_search)
    button_no = Button(frame_top, text='未售空', font=('楷体', 12), command=show_no)
    button_yes = Button(frame_top, text='已售空', font=('楷体', 12), command=show_yes)
    button = Button(frame_top, text='显示所有', font=('楷体', 12), command=show_all)
    button_no.pack(side='left', fill=X, expand=YES, padx=3, pady=5)
    button_yes.pack(side='left', fill=X, expand=YES, padx=3, pady=5)
    button.pack(side='left', fill=X, expand=YES, padx=3, pady=5)
    tree.bind("<Button-3>", popup)


def company_sale(window,userName):  # 查询公司票务信息
    companyId = get_companyId_by_user(userName)
    window.frame_right.destroy()
    window.frame_right = Frame(Main.flag.frame_bottom)
    window.frame_right.pack(side="right", fill=BOTH, expand=YES)
    frame_top = Frame(window.frame_right)
    frame_top.pack(side='top', fill=BOTH)
    frame_bottom = Frame(window.frame_right)
    frame_bottom.pack(side='bottom', fill=BOTH, expand=YES)
    Label(frame_top, text='查询统计销售信息：', font=('楷体', 18), fg='blue').pack(side='left', fill=BOTH, expand=YES)
    label_list = [Label(frame_top, text='顾客编号'), Entry(frame_top, width=10),
                  Label(frame_top, text='顾客姓名'), Entry(frame_top, width=10),
                  Label(frame_top, text='航班编号'), Entry(frame_top, width=10),
                  Label(frame_top, text='选择所属公司')]
    for label in label_list:
        label.pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    scrollbar = Scrollbar(frame_bottom)
    scrollbar.pack(side='right', fill=Y)
    tree = ttk.Treeview(frame_bottom, columns=list(range(9)), show='headings', yscrollcommand=scrollbar.set)
    column_name = ["订单号", "用户ID", "航班ID", "航空公司", "座位号", "乘客姓名",
                   "电话号码", "售票价格","销售日期"]
    for i in range(9):
        tree.column(str(i), width=50, anchor='w')
        tree.heading(str(i), text=column_name[i], anchor='w')
    tree.column('6', width=100)
    tree.column('5', width=80)
    tree.column('8', width=120)
    tree.column('7', width=80)
    tree.pack(fill=BOTH, expand=YES)

    for row in get_ticketData(" ticket.companyId = {}".format(companyId)):
        tree.insert('', 'end', values=row)
    scrollbar.config(command=tree.yview)

    def show_all(): # 显示所有销售信息
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_ticketData(" ticket.companyId = {}".format(companyId)):
            tree.insert('', 'end', values=new_row)

    def cno_search(event):  # 按顾客编号查找
        [tree.delete(item) for item in tree.get_children()]
        for row_search in get_ticketData(" userId = {} and  ticket.companyId = {}".format(label_list[1].get(),companyId)):
            tree.insert('', 'end', values=row_search)

    def cname_search(event):  # 按顾客姓名查找
        [tree.delete(item) for item in tree.get_children()]
        for row_search in get_ticketData(" passagerName like '%{}%' and  ticket.companyId = {}".format(label_list[3].get(),companyId)):
            tree.insert('', 'end', values=row_search)

    def pno_search(event):  # 按航班编号查找
        [tree.delete(item) for item in tree.get_children()]
        for row_search in get_ticketData(" flightId = {} and  ticket.companyId = {}".format(label_list[5].get(),companyId)):
            tree.insert('', 'end', values=row_search)

    popup_menu = Menu(frame_bottom, tearoff=0)

    def is_select():  # 判断Treeview中是否有行被选中
        flag = False
        for elem in tree.selection():
            flag = True
        return flag

    def price_sort():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_ticketData(" ticket.companyId = {} order by paidMoney".format(companyId)):
            tree.insert('', 'end', values=new_row)

    def date_sort():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_ticketData(" ticket.companyId = {}  order by paidTime".format(companyId)):
            tree.insert('', 'end', values=new_row)

    tree.heading("7", text="单价", command=lambda: price_sort())  # 点击表头排序
    tree.heading("8", text="销售日期", command=lambda: date_sort())  # 点击表头排序

    
    label_list[1].bind('<Key-Return>', cno_search)  # 回车 按顾客编号查询
    label_list[3].bind('<Key-Return>', cname_search)  # 回车 按顾客姓名查询
    label_list[5].bind('<Key-Return>', pno_search)  # 回车 按编号查询

    button = Button(frame_top, text='显示所有', font=('楷体', 14), command=show_all)
    button.pack(side='left', fill=X, expand=YES, padx=3, pady=5)


def search_sale(window,userName):  # 查询机场票务信息
    window.frame_right.destroy()
    window.frame_right = Frame(Main.flag.frame_bottom)
    window.frame_right.pack(side="right", fill=BOTH, expand=YES)
    frame_top = Frame(window.frame_right)
    frame_top.pack(side='top', fill=BOTH)
    frame_bottom = Frame(window.frame_right)
    frame_bottom.pack(side='bottom', fill=BOTH, expand=YES)
    Label(frame_top, text='查询统计销售信息：', font=('楷体', 18), fg='blue').pack(side='left', fill=BOTH, expand=YES)
    label_list = [Label(frame_top, text='顾客编号'), Entry(frame_top, width=10),
                  Label(frame_top, text='顾客姓名'), Entry(frame_top, width=10),
                  Label(frame_top, text='航班编号'), Entry(frame_top, width=10),
                  Label(frame_top, text='选择所属公司')]
    for label in label_list:
        label.pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    scrollbar = Scrollbar(frame_bottom)
    scrollbar.pack(side='right', fill=Y)
    tree = ttk.Treeview(frame_bottom, columns=list(range(9)), show='headings', yscrollcommand=scrollbar.set)
    column_name = ["订单号", "用户ID", "航班ID", "航空公司", "座位号", "乘客姓名",
                   "电话号码", "售票价格","销售日期"]
    for i in range(9):
        tree.column(str(i), width=50, anchor='w')
        tree.heading(str(i), text=column_name[i], anchor='w')
    tree.column('6', width=100)
    tree.column('5', width=80)
    tree.column('8', width=120)
    tree.column('7', width=80)
    tree.pack(fill=BOTH, expand=YES)

    for row in get_ticketData(1):
        tree.insert('', 'end', values=row)
    scrollbar.config(command=tree.yview)

    def show_all(): # 显示所有销售信息
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_ticketData(1):
            tree.insert('', 'end', values=new_row)

    def cno_search(event):  # 按顾客编号查找
        [tree.delete(item) for item in tree.get_children()]
        for row_search in get_ticketData(" userId = {}".format(label_list[1].get())):
            tree.insert('', 'end', values=row_search)

    def cname_search(event):  # 按顾客姓名查找
        [tree.delete(item) for item in tree.get_children()]
        for row_search in get_ticketData(" passagerName like '%{}%'".format(label_list[3].get())):
            tree.insert('', 'end', values=row_search)

    def pno_search(event):  # 按宠物编号查找
        [tree.delete(item) for item in tree.get_children()]
        for row_search in get_ticketData(" flightId = {}".format(label_list[5].get())):
            tree.insert('', 'end', values=row_search)

    popup_menu = Menu(frame_bottom, tearoff=0)

    def is_select():  # 判断Treeview中是否有行被选中
        flag = False
        for elem in tree.selection():
            flag = True
        return flag

    def alter():  # 修改销售信息
        if is_select():
            for elem in tree.selection():
                win = Toplevel()
                win.grab_set()  # 模态
                win.focus()
                center(win, 300, 600)
                labels = [Label(win, text='修改销售信息', fg='blue', font=('楷体', 14)),
                          Label(win, text='订单编号：' + tree.item(elem, 'values')[0]),
                          Label(win, text="乘客姓名"), Entry(win),
                          Label(win, text="手机号码"), Entry(win)]
                for l in labels:
                    l.pack()
                def confirm():
                    sql_update = "update ticket set passagerName='%s', passagerPhone='%s' where ticketId= '%s'"
                    data = (labels[3].get(), labels[5].get(), tree.item(elem, 'values')[0])
                    try:
                        execute_sql(sql_update % data)
                        tkinter.messagebox.showinfo("SUCCEED", "修改成功")
                        win.destroy()
                        show_all()
                    except pymysql.Error:
                        tkinter.messagebox.showerror("Failed", "修改失败")
                        win.focus()

                Button(win, text='确认修改', command=lambda: confirm()).pack(pady=20)
        else:
            tkinter.messagebox.showerror("ERROR", "未选择销售信息！")

    def delete():  # 删除宠物信息
        if is_select():
            if tkinter.messagebox.askokcancel('警告', '确认删除该销售信息吗？'):
                for elem in tree.selection():
                    try:
                        execute_sql("delete from ticket where ticketId='{}'".format(tree.item(elem, 'values')[0]))
                        tkinter.messagebox.showinfo('Succeed', '删除成功！')
                        show_all()
                    except pymysql.Error:
                        tkinter.messagebox.showerror('Failed', '删除失败!')
        else:
            tkinter.messagebox.showerror('ERROR', '未选择销售信息！')

    def popup(event):  # 弹出右键菜单
        popup_menu.post(event.x_root, event.y_root)

    def price_sort():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_ticketData("1 order by paidMoney"):
            tree.insert('', 'end', values=new_row)

    def date_sort():
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_ticketData("1 order by paidTime"):
            tree.insert('', 'end', values=new_row)

    tree.heading("7", text="单价", command=lambda: price_sort())  # 点击表头排序
    tree.heading("8", text="销售日期", command=lambda: date_sort())  # 点击表头排序

    popup_menu.add_command(label='修改', command=lambda: alter())
    popup_menu.add_separator()
    popup_menu.add_command(label='删除', command=lambda: delete())

    label_list[1].bind('<Key-Return>', cno_search)  # 回车 按顾客编号查询
    label_list[3].bind('<Key-Return>', cname_search)  # 回车 按顾客姓名查询
    label_list[5].bind('<Key-Return>', pno_search)  # 回车 按宠物编号查询

    def show(event):
        [tree.delete(item) for item in tree.get_children()]
        for new_row in get_ticketData(" ticket.companyId ={}".format(cmb.get())):
            tree.insert('', 'end', values=new_row)

    cmb = ttk.Combobox(frame_top, value=get_companyId('ticket'), state='readonly', width=5)
    cmb.pack(side="left", fill=X, expand=YES, padx=3, pady=2)
    cmb.bind("<<ComboboxSelected>>", show)

    button = Button(frame_top, text='显示所有', font=('楷体', 14), command=show_all)
    button.pack(side='left', fill=X, expand=YES, padx=3, pady=5)
    tree.bind("<Button-3>", popup)


def add_sale(win):  # 添加订单信息
    win.frame_right.destroy()
    win.frame_right = Frame(Main.flag.frame_bottom)
    win.frame_right.pack(side='right', fill=BOTH, expand=YES)
    Label(win.frame_right, text="添  加   订   单   信   息：", fg='blue', font=('华文彩云', 16)).pack(pady=10)
    string_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    Label(win.frame_right, text='订单编号：' + string_time).pack(pady=10)
    Label(win.frame_right, text="销售日期：" + time.strftime("%Y-%m-%d", time.localtime())).pack(pady=10)
    Label(win.frame_right, text="选择航班编号：", fg='MediumBlue', font=("楷体", 14)).pack(pady=10)
    cursor_c = execute_sql("SELECT flightId FROM flight;")
    no_c = []
    for result in cursor_c.fetchall():  # 查询所有航班编号添加到下拉列表供用户选择
        no_c.append(result[0])
    cmb_c = ttk.Combobox(win.frame_right, value=no_c, state='readonly')
    cmb_c.pack(pady=2)
    string_show_c = [StringVar(), StringVar(), StringVar(), StringVar(),StringVar()]
    label_show_c = [Label(win.frame_right), Label(win.frame_right), Label(win.frame_right), Label(win.frame_right),Label(win.frame_right)]
    init_name_c = ['航空公司:', '出发地:', '目的地:', '出发时间:','票价：']
    for i in range(5):
        string_show_c[i].set(init_name_c[i])
        label_show_c[i]['textvariable'] = string_show_c[i]
        label_show_c[i].pack(pady=2)

    def show_c(event):
        global string_time
        string_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        sql_select = "SELECT companyName,departure,terminal,leaveTime,ticketMoney FROM flight,company where flight.companyId =company.companyId and flightId={};"
        result_row = execute_sql(sql_select.format(cmb_c.get())).fetchone()
        for j in range(5):
            string_show_c[j].set(init_name_c[j] + str(result_row[j]))

    cmb_c.bind("<<ComboboxSelected>>", show_c)

    Label(win.frame_right, fg='MediumBlue', font=("楷体", 14), text="选择购票用户编号：").pack(pady=10)
    cursor_p = execute_sql("SELECT userId FROM customerUser")
    no_p = []
    for result in cursor_p.fetchall():  # 查询所有未售出宠物编号名添加到下拉列表供用户选择
        no_p.append(result[0])
    cmb_p = ttk.Combobox(win.frame_right, value=no_p, state='readonly')
    cmb_p.pack(pady=2)
    string_show_p = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
    label_show_p = [Label(win.frame_right), Label(win.frame_right),
                    Label(win.frame_right),Label(win.frame_right)]
    init_name_p = ['用户名:', '用户类型:', '积分:','优惠折扣：']
    for i in range(4):
        string_show_p[i].set(init_name_p[i])
        label_show_p[i]['textvariable'] = string_show_p[i]
        label_show_p[i].pack(pady=2)

    def show_p(event):
        sql_select = "SELECT userName,vip,point FROM customerUser where userId={};"
        result_row = execute_sql(sql_select.format(cmb_p.get())).fetchone()
        for j in range(3):
            string_show_p[j].set(init_name_p[j] + str(result_row[j]))
        if result_row[1] == 1.0:
            string_show_p[1].set(init_name_p[1] + 'VIP注册会员')
            string_show_p[3].set(init_name_p[3] + str(10*get_discount(result_row[0]))+"折")
        else:
            string_show_p[1].set(init_name_p[1] + '未注册会员')
            string_show_p[3].set(init_name_p[3] + '无')
        

    cmb_p.bind("<<ComboboxSelected>>", show_p)

    labels = [Label(win.frame_right, text="乘客姓名"), Entry(win.frame_right),
              Label(win.frame_right, text="手机号码"), Entry(win.frame_right),
              Label(win.frame_right, text="座位号"), Entry(win.frame_right)]
    for l in labels:
        l.pack()
    
    def confirm():
        global string_time
        _companyId, _money = execute_sql("SELECT companyId,ticketMoney FROM flight where flightId={};".format(cmb_c.get())).fetchone()
        money = _money*get_discount(get_userName(cmb_p.get()))
        leftTicket = get_leftTicket(cmb_c.get())-1
        if leftTicket<0:
            tkinter.messagebox.showinfo("提示", "余票不足，无法购买！")
            return 
        new_points = get_points(get_userName(cmb_p.get()))+int(money)
        sql = "insert into ticket values(%s,%s, %s,%s, '%s','%s',%s,%s,'%s');"
        sql2= "update flight set leftTicket = {} where flightId = {}".format(leftTicket,cmb_c.get())
        sql3= "update customerUser set point = {} where userName = '{}'".format(new_points,get_userName(cmb_p.get()))
        data = (string_time, cmb_p.get(),cmb_c.get(),_companyId,labels[5].get(),labels[1].get(),labels[3].get(),money,time.strftime("%Y/%m/%d", time.localtime()))
        try:
            execute_sql(sql % data)
            execute_sql(sql2)
            execute_sql(sql3)
            tkinter.messagebox.showinfo("SUCCEED", "添加成功")
        except pymysql.Error:
            tkinter.messagebox.showerror("Failed", "添加失败")

    Button(win.frame_right, text='确认添加', command=lambda: confirm()).pack(pady=20)


class FrameLeft(Frame):  # 左侧菜单栏
    def __init__(self, master, user):
        self.userType = user[0]
        self.userName = user[1]
        Frame.__init__(self, master, bg='gray', width=180, borderwidth=2)
        self.pack_propagate(False)  #固定frame大小
        self.create()

    def create(self):
        if self.userType == "customerUser":
            Button(self, text="主      页", bg='#7fffd4', font=('华文琥珀', 16), command=lambda: go_home(Main.flag)).pack(fill=X)
            Label(self, text="统计信息", bg='maroon1', fg='blue', font=("楷体", 16)).pack(fill=X)
            Button(self, text="公告信息", command=lambda: personal_notice(Main.flag,self.userName)).pack(fill=X)
            Button(self, text="我的信息", command=lambda: personal_data(Main.flag,self.userName)).pack(fill=X)
            Button(self, text="航班信息", command=lambda: personal_flight(Main.flag, self.userName)).pack(fill=X)
            Button(self, text="我的机票", command=lambda: personal_ticket(Main.flag,self.userName)).pack(fill=X)
        elif self.userType == "companyUser":
            Button(self, text="主      页", bg='#7fffd4', font=('华文琥珀', 16), command=lambda: go_home(Main.flag)).pack(fill=X)
            Label(self, text="统计信息", bg='maroon1', fg='blue', font=("楷体", 16)).pack(fill=X)
            Button(self, text="公司航班", command=lambda: company_flight(Main.flag,self.userName)).pack(fill=X)
            Button(self, text="售票信息", command=lambda: company_sale(Main.flag,self.userName)).pack(fill=X)
            Label(self, text="录入信息", bg='maroon1', fg='blue', font=("楷体", 16)).pack(fill=X)
            Button(self, text="添加航班", command=lambda: self.add_flight(self.userName)).pack(fill=X)
        else:
            Button(self, text="主      页", bg='#7fffd4', font=('华文琥珀', 16), command=lambda: go_home(Main.flag)).pack(fill=X)
            Label(self, text="统计信息", bg='maroon1', fg='blue', font=("楷体", 16)).pack(fill=X)
            Button(self, text="顾客信息", command=lambda: search_client(Main.flag)).pack(fill=X)
            Button(self, text="机场航班", command=lambda: airport_flight(Main.flag,self.userName)).pack(fill=X)
            Button(self, text="票务信息", command=lambda: search_sale(Main.flag,self.userName)).pack(fill=X)
            Label(self, text="录入信息", bg='maroon1', fg='blue', font=("楷体", 16)).pack(fill=X)
            Button(self, text="添加旅客", command=lambda: self.add_user()).pack(fill=X)
            Button(self, text="添加销售信息", command=lambda: add_sale(Main.flag)).pack(fill=X)
        def quit_sys():
            if tkinter.messagebox.askokcancel('提示', '确认退出吗？'):
                sys.exit(0)

        Button(self, text="退出系统", fg='blue', font=('楷体', 14), command=lambda: quit_sys()).pack(fill=X)

    @staticmethod
    def add_user():  # 添加用户信息事件
        win = Toplevel()
        win.grab_set()
        win.focus()
        center(win, 300, 400)
        labels = [Label(win, text='旅客编号'), Entry(win),
                  Label(win, text="账号"), Entry(win),
                  Label(win, text="密码"), Entry(win)]
        for label in labels:
            label.pack()

        labels_vip = [  Label(win, text='姓名'), Entry(win),
            Label(win, text="手机号"), Entry(win),
            Label(win, text="性别"), Entry(win)]

        Label(win, text="是否注册VIP?", fg='MediumBlue', font=("楷体", 12)).pack(pady=10)
        choose = ttk.Combobox(win, value=['是','否'], state='readonly')
        choose.pack(pady=2)

   
        def show_choose(event):
            if choose.get() == '是':
                for label in labels_vip:
                    label.pack()
            else:
                pass
            Button(win, text='确认', command=lambda: confirm()).pack()
        
        choose.bind("<<ComboboxSelected>>", show_choose)



        def confirm():  # 确认添加事件4
            if choose.get() == "否":
                sql = "insert into customerUser values('%s', '%s', '%s', '0.0', '0','None','None','None');"
                data = [labels[1].get(),labels[3].get(),labels[5].get()]
            else:
                sql = "insert into customerUser values('%s', '%s', '%s', '1.0', '0','%s','%s','%s');"
                data = [labels[1].get(),labels[3].get(),labels[5].get(),labels_vip[1].get(),labels_vip[3].get(),labels_vip[5].get()]
            try:
                execute_sql(sql % tuple(data))  # 字符串格式化
                tkinter.messagebox.showinfo("SUCCEED", "录入成功！")
                win.destroy()
            except pymysql.Error:
                tkinter.messagebox.showerror("ERROR", "输入有误！")
                win.focus()


    @staticmethod
    def add_flight(v):  # 添加航班事件
        string_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        win = Toplevel()
        win.grab_set()
        win.focus()
        center(win, 300, 600)
        choose_p1 = ttk.Combobox(win, value=get_airportName('all'), state='readonly')
        choose_p2 = ttk.Combobox(win, value=get_airportName('all'), state='readonly')
        choose_co = ttk.Combobox(win, value=get_companyName(get_companyId_by_user(v)), state='readonly')
        labels = [Label(win, text='航班编号：' + string_time),
                  Label(win, text="飞机类型"), Entry(win),
                  Label(win, text="出发地"), choose_p1,
                  Label(win, text="目的地"), choose_p2,
                  Label(win, text="起飞时间"), Entry(win),
                  Label(win, text="到达时间"), Entry(win),
                  Label(win, text="可售票数"), Entry(win), 
                  Label(win, text="总票数"), Entry(win),
                  Label(win, text="票价"), Entry(win),
                  Label(win, text="所属公司"), choose_co]
        for label in labels:
            label.pack()


        def confirm():  # 确认添加事件
            sql = "insert into flight values('%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s', '%s')"
            data = [string_time]
            for text in labels[2::2]:
                data.append(text.get())
            data[2] = get_airportId2(data[2])
            data[3] = get_airportId2(data[3])
            data[-1] = get_companyId(data[-1])
            try:
                execute_sql(sql % tuple(data))
                tkinter.messagebox.showinfo("SUCCEED", "录入成功！")
                win.destroy()
            except pymysql.Error:
                tkinter.messagebox.showerror("ERROR", "输入有误！")
                win.focus()

        Button(win, text='确认', command=lambda: confirm()).pack()


def sign_in(event):  # 登录
    cursor= get_connect().cursor()
    user = [userType.get(),entry.get()]
    sql = "select password from "+userType.get()+" where userName='" + entry.get()+"'"

    try:
        cursor.execute(sql)
        password_input = entry_password.get()  # 获取用户输入的密码
        password_db = (cursor.fetchone())[0]  # 获取数据中的密码
        if password_input == password_db:  # 判断用户输入的密码与数据库中的是否一致
            tkinter.messagebox.showinfo(title="succeed", message="登陆成功")
            login.destroy()  # 销毁当前窗口
            new_win = Tk()  # 进入主界面
            # center(login, login.winfo_screenwidth(,) login.winfo_screenheight())  # 最大化，效果不好
            center(new_win, 1200, 800)
            new_win.title("民航售票管理系统")
            app = Main(user)
            Main.flag = app
            center(app.master, 1200, 800)
        else:
            tkinter.messagebox.showerror(title="failed", message="账号或者密码错误1")
    except (pymysql.Error, TypeError):
        tkinter.messagebox.showerror(title="failed", message="账号或密码错误2")


login = Tk()  # 登陆界面
center(login, 600, 440)
login.resizable(0, 0)
login.title("民航票务系统")

fm1 = Frame(login)
fm1.place(x=280, y=400)
group = LabelFrame(fm1,text="请选择您的身份",padx=5,pady=5)
group.pack(padx=10,pady=10)
userType = StringVar()
userType.set('customerUser')
radio = tkinter.Radiobutton(group,variable = userType,value ='customerUser',text='购票用户')
radio.pack()
radio = tkinter.Radiobutton(group,variable = userType,value ='airportUser',text='机场管理员')
radio.pack()
radio = tkinter.Radiobutton(group,variable = userType,value ='companyUser',text='航空公司管理员')
radio.pack()
fm1.pack(side=LEFT, fill=BOTH, expand=YES)

fm2 = Frame(login)
fm2.place(x=180, y=200)
label_1 = Label(fm2, text="账号：", font=("宋体", 12))
label_1.grid(row=0, column=0, pady=5)
entry = Entry(fm2, show=None, font=("Arial", 12))
entry.grid(row=0, column=1)
entry.focus()
label_2 = Label(fm2, text="密码：", font=("宋体", 12))
label_2.grid(row=1, column=0)
entry_password = Entry(fm2, show="*", font=("Arial", 12))
entry_password.grid(row=1, column=1, pady=5)
entry_password.bind('<Key-Return>', sign_in)  # 密码输入框回车登录
button_sign_in = Button(fm2, text='     登    录      ', fg='black', command=lambda: sign_in(None))
button_sign_in.grid(row=2, column=1)

login.mainloop()
