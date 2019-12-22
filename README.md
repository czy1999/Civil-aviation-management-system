# 一、 概述

民航售票管理系统主要分为机场、航空公司和客户三方的服务。航空公司提供航线和飞机的资料，机场则对在本机场起飞和降落的航班和机票进行管理，而客户能得到的服务应该有航班线路和剩余票数的查询，以及网上订票等功能。客户又可以分为两类，一类是普通客户，对于普通客户只有普通的查询功能和订票功能，没有相应的机票优惠，另一种是经常旅客，需要办理注册手续，但增加了里程积分功能和积分优惠政策。机场还要有紧急应对措施，在航班出现延误时，要发送相应的信息。

本系统能够完成如下功能：

**订票用户**

(1)   查询当前的航班信息，包括航班时间，机型，价格，余票数量等数据，并且可以根据不同得选择对机票进行筛选，选择购买后积分自动累加。

(2)   查询自己已经订购得机票，并且可以修改乘客或者进行退票。

(3)   查询自己得个人信息，可以修改账户密码，未注册的用户可以自行注册VIP。

 

**航空公司管理员**

(1)  查看公司的航班信息，包括航班时间，机型，价格，余票数量等，并且可以进行筛选。。

(2)  查询公司航班的售票情况，包括航班，乘客，价格，付款金额等数据，并且可以进行筛选。

(3)  添加或修改公司的航班信息，包括航班时间，机型，价格，余票数量等。

 

**机场管理员**

(1)  查询当前所有的顾客信息，可以对顾客信息进行修改或者注册新用户。

(2)  查询涉及本机场的航班，并且可以对航班进行修改。

(3)  对发生异动的航班，管理员可以选择对相关用户发送公告，告知其相关信息。

(4)  可以查询或修改当前的售票信息，并且可以添加销售信息。

# 二、 实验环境

本系统开发平台及运行环境如下：

系统开发语言：Python

数据库管理软件：SQL Server 2017

运行平台：Windows10

# 三、 实验内容与步骤

## 3.1系统需求分析

## 3.1.1系统工作原理

1)   注册。由用户向机场管理员申请注册，由管理员将信息表单提交到系统，由控制层调用数据逻辑层操作数据库，完成用户的注册。

2)   用户登录。对用户输入的登录信息进行验证，判定用户选择的用户类别和输入的用户名和密码是否匹配，若不匹配则无权使用该系统，反之则能合法使用系统。

3)   修改个人信息。用户对可以对个人信息进行查询及修改。

4)   航班查询。用户对数据库中航班信息进行查询，显示满足用户查询条件的航班信息。

5)   订票。用户查询到自己需要的航班信息后可进行订购操作，首先查询用户所享受的优惠，确定付款金额后，系统会将相关信息一并发送到机票订购模块，将信息写入订单信息存储，并且运行积分模块，进行积分的累计。

6)   修改信息。此工作接受用户的修改信息，根据用户ID和预订的航班号，对满足条件的已预订机票进行修改处理。

7)   退票。此工作接受用户的退票信息，根据用户ID和预订的航班号，对满足退票条件的已预订机票进行退票处理，并且扣除所加积分。

8)   航班信息录入。此工作接收由航空公司管理员录入的航班信息，并将其导入数据库进行存储，供用户查询和预订。

9)   航班信息更新。此工作接收管理员对某些需要更新的航班信息的更新操作，并修改存储在数据库中相关信息。

10)  订单查询。用户可以查询自己已完成的或未出行的订单，管理员可以查看所属用户的所有订单。

 

### 3.1.3表的设计

本系统采用MySQL数据库。在系统中创建test数据库包含8张表，各个表的详细设计如下：

**公司管理员信息****表**

表名：companyUser

公司管理员信息表

| 属性名    | 类型        | 允许为空 | 主键 | 描述     |
| --------- | ----------- | -------- | ---- | -------- |
| userId    | INT         | No       | 主键 | 用户编号 |
| userName  | VARCHAR(50) | Yes      |      | 用户名   |
| password  | VARCHAR(50) | Yes      |      | 密码     |
| companyId | INT         | Yes      | 外键 | 所属公司 |

​                  

**机场管理员信息表**

表名：airportUser

机场管理员信息表

| 属性名    | 类型        | 允许为空 | 主键 | 描述     |
| --------- | ----------- | -------- | ---- | -------- |
| userId    | INT         | No       | 主键 | 用户编号 |
| userName  | VARCHAR(50) | No       |      | 用户名   |
| password  | VARCHAR(50) | No       |      | 密码     |
| airportId | INT         | No       | 外键 | 所属机场 |

 

**顾客信息表**

表名：customerUser

顾客信息表

| 属性名   | 类型        | 允许为空 | 主键 | 描述         |      |
| -------- | ----------- | -------- | ---- | ------------ | ---- |
| userId   | INT         | No       | 主键 | 用户编号     |      |
| userName | VARCHAR(50) | No       |      | 用户名       |      |
| password | VARCHAR(50) | No       |      | 密码         |      |
| Vip      | INT         | No       |      | 是否注册用户 |      |
| Point    | INT         | No       |      | 积分         |      |
| realName | VARCHAR(50) | Yes      |      | 姓名         |      |
| phone    | VARCHAR(50) | Yes      |      | 手机号       |      |
| sex      | VARCHAR(50) | Yes      |      | 性别         |      |

 

 

 

 

**公告信息表**

表名：board

公告信息表

| 属性名   | 类型 | 允许为空 | 主键 | 描述         |
| -------- | ---- | -------- | ---- | ------------ |
| boardId  | INT  | No       | 主键 | 公告编号     |
| flightId | INT  | No       | 外键 | 涉及航班编号 |
| dueTime  | INT  | No       |      | 截止日期     |

 

**机场信息表**

表名：airport

机场信息表

| 属性名      | 类型        | 允许为空 | 主键 | 描述     |
| ----------- | ----------- | -------- | ---- | -------- |
| airportId   | INT         | No       | 主键 | 机场编号 |
| airportName | VARCHAR(50) | No       |      | 机场名称 |

 

**公司信息表**

表名：company

公司信息表

| 属性名      | 类型        | 允许为空 | 主键 | 描述     |
| ----------- | ----------- | -------- | ---- | -------- |
| companyId   | INT         | No       | 主键 | 公司编号 |
| companyName | VARCHAR(50) | No       |      | 公司名称 |

 

**机票销售信息表**

表名：ticket

表3-4 机票销售信息表

| 属性名        | 类型        | 允许为空 | 主键 | 描述       |
| ------------- | ----------- | -------- | ---- | ---------- |
| ticketId      | INT         | No       | 主键 | 机票编号   |
| userId        | INT         | No       | 外键 | 顾客编号   |
| flightId      | INT         | No       | 外键 | 航班编号   |
| companyId     | INT         | No       | 外键 | 航班公司   |
| seatNumber    | INT         | No       |      | 座位号     |
| passagerName  | VARCHAR(50) | No       |      | 乘客姓名   |
| passagerPhone | VARCHAR(50) | No       |      | 乘客手机号 |
| paidMoney     | INT         | No       |      | 付款金额   |
| paidTime      | VARCHAR(50) | No       |      | 付款时间   |

 

 

 

**航班信息表**

表名：flight

表3-5 宠物用品销售信息表

| 属性名      | 类型        | 允许为空 | 主键 | 描述       |
| ----------- | ----------- | -------- | ---- | ---------- |
| flightID    | INT         | No       | 主键 | 航班号     |
| plane       | VARCHAR(50) | No       |      | 飞机机型   |
| departure   | INT         | No       | 外键 | 出发地编号 |
| terminal    | INT         | No       | 外键 | 目的地编号 |
| leaveTime   | VARCHAR(50) | No       |      | 出发时间   |
| arrivetime  | VARCHAR(50) | No       |      | 到达时间   |
| leftTicket  | INT         | No       |      | 余票数量   |
| totalTicket | INT         | No       |      | 总票数     |
| ticketMoneu | INT         | No       |      | 票价       |
| companyID   | INT         | No       | 外键 | 所属公司   |



# 四、 程序运行展示
![](images/image.png)
