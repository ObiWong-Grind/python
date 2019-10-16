"""
    数据库操作
"""


import pymysql


class OperationDB:
    """
        数据库处理
    """
    def __init__(self):
        self.__db, self.__cur = self.__connect_db()

    def __connect_db(self):
        """
            启动数据库
        """
        db = pymysql.connect(host="localhost", port=3306, user="root", password="122336978", database="diagrams", charset="utf8")
        cur = db.cursor()
        return db, cur

    def __close_db(self):
        self.__cur.close()
        self.__db.close()

    def __select_login_time(self, user_id):
        """
            修改上线时间
        :param user_id: 用户id
        """
        try:
            sql = "update user set login_time=now() where id=%s limit 1;"
            self.__cur.execute(sql, [user_id])
            self.__db.commit()
        except Exception as e:
            self.__db.rollback()
            print("2", e)
        finally:
            self.__cur.close()
            self.__db.close()

    def select_login_info(self, account, password):
        """
            使用账号、密码通过sql语句执行 匹配账号密码是否正确
        """
        sql = "select id,user_name from user where account_phone=%s and password=%s limit 1;"
        self.__cur.execute(sql, [account, password])
        data = self.__cur.fetchone()
        if data:  # 如果 data 有返回值
            self.__select_login_time(data[0])  # 修改用户上线时间
            return data  # 将查询出的 id 和 user_name 返回
        else:
            return False

    def insert_user(self, phone, password, user_name):
        """
            验证通过，往数据库插入新的用户数据
        :param phone: 手机账户
        :param password: 密码
        :param user_name: 用户名
        """
        try:
            sql = "insert into user (account_phone,password,user_name) values (%s,%s,%s);"
            self.__cur.execute(sql, [phone, password, user_name])
            self.__db.commit()
        except Exception as e:
            self.__db.rollback()
            print("1", e)
            return False
        else:
            result = self.select_login_info(phone, password)
            if result:
                return result
            self.__close_db()

    def select_phone(self, phone):
        """
            查询注册账户是否在
        :return: False 手机号被占用，True 未被占用
        """
        sql = "select account_phone from user where account_phone=%s;"
        self.__cur.execute(sql, [phone])
        data = self.__cur.fetchone()
        if data:  # 如果data有值表示 手机号已被占用
            self.__close_db()
            return False
        else:
            self.__close_db()
            return True

    def insert_history(self, user_id, user_name, option_key, request, o_diagram, f_diagram, s_diagram, t_diagram):
        """
            插入数据库
        :param user_id: 用户id
        :param user_name: 用户姓名
        :param option_key: 求卦选项
        :param request: 问卦
        :param o_diagram: 原本卦
        :param f_diagram: 本卦
        :param s_diagram: 互卦
        :param t_diagram: 变化
        """
        try:
            sql = "insert into three_diagrams (user_id,user_name,option_key,request,o_diagram,f_diagram,s_diagram,t_diagram) values (%s,%s,%s,%s,%s,%s,%s,%s);"
            self.__cur.execute(sql, [user_id, user_name, option_key, request, o_diagram, f_diagram, s_diagram, t_diagram])
            self.__db.commit()
        except Exception as e:
            self.__db.rollback()
            print(e)
        finally:
            self.__close_db()





