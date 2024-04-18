import datetime
import pymysql


def create(name, trade_no):
    mysql = pymysql.connect(host='39.108.128.154',
                            port=3307,
                            user='b2bwings',
                            password='b2bwings666!',
                            database='cqjy-account')
    cursor = mysql.cursor()
    time = (datetime.datetime.now()).strftime('%Y%m%d%H%M%S')
    time1 = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
    sql = ("INSERT INTO `cqjy-account`.`t_sub_account`(`sub_account_id`, `app_id`, `app_name`, `sub_app_id`, "
           "`sub_account_no`, `sub_account_name`, `sub_req_no`, `organization_name`, `organization_id`, "
           "`main_account_no`, `account_bank_code`, `main_account_name`, `open_bank_name`,  `project_trade_no`, "
           "`auth_code`, `account_status`, `gmt_create`, `project_name`) "
           "VALUES (" + time + ", 'gdnccqjy', '广东省农村产权流转交易管理服务平台', '100000', '95588" + time + "', "
           "'八赏冒乐蹬饥符曾绍亥猴睹崎等佑', \'" + time + "\', '清远市清新区集体资产交易中心', 1531213778436427778,"
           "'3602023929200100926', '102', '八赏冒乐蹬饥符曾绍亥猴睹崎等佑', "
           "'中国工商银行广州支行',  \'" + trade_no + "\', \'" + time + "\', '00', '" + time1 + "', '" + name +
           "');")
    print("success")
    cursor.execute(sql)
    try:
        mysql.commit()
    except Exception as e:
        mysql.rollback()
    cursor.close()
    mysql.close()


if __name__ == '__main__':
    while 1 == 1:
        name, trade_no = (input("输入项目名和项目编号：").split())
        create(name, trade_no)
