import pymysql
import sqlite3
import time

def get_connect():  # 获取连接
    connect = sqlite3.connect('test.db')
    # connect = pymssql.connect(host='127.0.0.1' ,user='test' ,password = 'test',database='test', charset='utf8')
    return connect


def execute_sql(sql):  # 执行SQL语句并返回执行结果的游标
    connect = get_connect()
    cursor = connect.cursor()
    cursor.execute(sql)
    connect.commit()
    return cursor


def get_airportName(num):
    if num == 'all':
        sql = "select airportName from airport "
        result = []
        for r in execute_sql(sql).fetchall():
            result.append(r[0])
    else:
        sql = "select airportName from airport where airportId = "+str(num)
        result = execute_sql(sql).fetchone()[0]
    return result

def get_airportId1(name):
    sql = "select airportId from airport where airportName = '"+ str(name)+"'"
    result = execute_sql(sql).fetchone()[0]
    return result


def get_companyName(num):
    if num == 'all':
        sql = "select companyName from company "
        result = []
        for r in execute_sql(sql).fetchall():
            result.append(r[0])
    else:
        sql = "select companyName from company where companyId = "+str(num)
        result = execute_sql(sql).fetchone()[0]
    return result

def get_companyId_by_user(v):
    sql = "select companyId from companyUser where userName = '"+str(v)+"'"
    result = execute_sql(sql).fetchone()[0]
    return result

def get_companyId(name):
    if name == 'ticket':
        result = []
        sql = "select distinct companyId from ticket"
        for r in execute_sql(sql).fetchall():
            result.append(r[0])
    else:
        sql = "select companyId from company where companyName = '"+ str(name)+"'"
        result = execute_sql(sql).fetchone()[0]
    return result

def get_userData(conditiom):
    result = execute_sql("SELECT userId,realName,sex,phone,point FROM customerUser WHERE "+str(conditiom))
    return result

def get_userId(username):
    sql = "select userId from customerUser where userName = '"+ str(username)+"'"
    result = str(execute_sql(sql).fetchone()[0])
    return result

def get_userName(userId):
    sql = "select userName from customerUser where userId = '"+ str(userId)+"'"
    result = str(execute_sql(sql).fetchone()[0])
    return result

def get_airportId(username):
    sql = "select airportId from airportUser where userName = '"+ str(username)+"'"
    result = str(execute_sql(sql).fetchone()[0])
    return result

def get_airportId2(airportName):
    sql = "select airportId from airport where airportName = '"+ str(airportName)+"'"
    result = str(execute_sql(sql).fetchone()[0])
    return result

def transform_airport_ID(v):
    r = []
    for i,v in enumerate(v):
        r.append([])
        for j in v:
            r[i].append(j)

    for i,v in enumerate(r):
        r[i][2] = get_airportName(r[i][2])
        r[i][3] = get_airportName(r[i][3])
        r[i][5] = get_companyName(r[i][5])
    return r

def get_flightData(conditiom):
    result = execute_sql("SELECT flightId,plane,departure,terminal,ticketMoney,companyId,leaveTime,leftTicket FROM flight WHERE "+str(conditiom))
    return transform_airport_ID(result)

def get_flightData2(companyId,conditiom):
    result = execute_sql("SELECT flightId,plane,departure,terminal,ticketMoney,companyId,leaveTime,leftTicket FROM flight WHERE companyId = " + str(companyId) +" and "+str(conditiom))
    return transform_airport_ID(result)

def get_airport_flightData(airportId,conditiom):
    result = execute_sql("SELECT flightId,plane,departure,terminal,ticketMoney,companyId,leaveTime,leftTicket FROM flight WHERE (departure = "+str(airportId)+" or terminal = "+str(airportId)+" ) and "+str(conditiom))
    return transform_airport_ID(result)

def get_ticketData(conditiom):
    result = execute_sql("SELECT ticketId,userId,flightId,companyName,seatNumber,passagerName,passagerPhone,paidMoney,paidTime from ticket, company where ticket.companyId = company.companyId and "+str(conditiom))
    return result

def get_leftTicket(flightId):
    sql = "select leftTicket from flight where flightId = '"+ str(flightId)+"'"
    result = execute_sql(sql).fetchone()[0]
    return result

def VIPorNOT(username):
    sql = "select vip from customerUser where userName = '{}'".format(username)
    result = execute_sql(sql).fetchone()[0]
    if result == 1.0:
        return True
    else:
        return False

def get_seat(num):
    result = []
    seats = []
    sql = "select seatNumber from ticket where flightId = '{}'".format(num)
    for r in execute_sql(sql).fetchall():
        result.append(r[0])
    for i in range(1,51):
        if i not in result:
            seats.append(i)
    return seats

def get_points(username):
    sql = "select point from customerUser where userName = '{}'".format(username)
    result = execute_sql(sql).fetchone()[0]
    return result


def is_saled(flightId): # 查询航班是否有顾客购买，作为能否删除的依据
    sql = "select count(*) from ticket where flightId = '{}'".format(flightId)
    result = execute_sql(sql).fetchone()[0]
    return result

def add_board(flightId,dueTime):
    string_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    _time = time.strptime(dueTime, '%Y/%m/%d')
    duetime = time.strftime("%Y%m%d%H%M%S", _time)
    sql = "insert into board values('{}','{}','{}');".format(string_time,flightId,duetime)
    execute_sql(sql)

def get_board(userid):
    sql = "select * from customer_notice where userId = {}".format(userid)
    r = execute_sql(sql).fetchall()
    result = []
    for i in r:
        result.append([i[0],i[1],"您好，本次航班时刻有所调整，请及时在我的机票中查看~"])
    return result

def get_discount(userName):
    points = get_points(userName)
    if points >= 10000:
        return 0.8
    elif points >= 5000:
        return 0.9
    else:
        return 1

