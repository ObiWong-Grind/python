"""
    注册模块
"""


from login_and_sign.login import *
from tools.passwd import *


class DiagramSign:
    """
        注册
    """
    def __init__(self, phone):
        """
            初始化
        :param phone: 手机号
        """
        self._phone = phone
        self._login = DiagramLogin()
        self.__connect_db()

    def __connect_db(self):
        """
            启动数据库
        """
        self._db = pymysql.connect(host="localhost", port=3306, user="root", password="122336978", database="diagrams", charset="utf8")
        self._cur = self._db.cursor()

    def __close_db(self):
        """
            数据库关闭
        """
        self._cur.close()
        self._db.close()

    def __select_login_info(self, account, password):
        """
            使用账号、密码通过sql语句执行 匹配账号密码是否正确
        """
        sql = "select id,user_name from user where account_phone=%s and password=%s limit 1;"
        self._cur.execute(sql, [account, password])
        data = self._cur.fetchone()
        if data:  # 如果 data 有返回值
            self._login.select_login_time(data[0])  # 修改用户上线时间
            return data  # 将查询出的 id 和 user_name 返回
        else:
            return False

    def insert_user(self, password, user_name):
        """
            验证通过，往数据库插入新的用户数据
        :param password: 密码
        :param user_name: 用户名
        """
        password = PassWordHash().hashpasswd(self._phone, password)
        try:
            sql = "insert into user (account_phone,password,user_name) values (%s,%s,%s);"
            self._cur.execute(sql, [self._phone, password, user_name])
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print("1", e)
            return False
        else:
            result = self.__select_login_info(self._phone, password)
            if result:
                return result
            self.__close_db()

    def select_phone(self):
        """
            查询注册账户是否在
        :return: False 手机号被占用，True 未被占用
        """
        sql = "select account_phone from user where account_phone=%s;"
        self._cur.execute(sql, [self._phone])
        data = self._cur.fetchone()
        if data:  # 如果data有值表示 手机号已被占用
            self.__close_db()
            return False
        else:
            self.__close_db()
            return True

