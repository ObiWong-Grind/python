"""
    登录模块
"""


import pymysql


class DiagramLogin:
    """
        登录模块
    """
    def __init__(self):
        """
            初始化
        """
        self.__connect_db()

    def __connect_db(self):
        """
            启动数据库
        """
        self._db = pymysql.connect(host="localhost", port=3306, user="root", password="r0260zgmf", database="diagrams",
                                   charset="utf8")
        self._cur = self._db.cursor()

    def __login_time(self, user_id):
        """
            修改上线时间
        :param user_id: 用户id
        """
        try:
            sql = "update user set login_time=now() where id=%s limit 1;"
            self._cur.execute(sql, [user_id])
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print(e)
        finally:
            self._cur.close()
            self._db.close()

    def match_login_info(self, account, password):
        """
            使用账号、密码通过sql语句执行 匹配账号密码是否正确
        """
        sql = "select id,user_name from user where account_phone=%s and password=%s limit 1;"
        self._cur.execute(sql, [account, password])
        data = self._cur.fetchone()
        if data:  # 如果 data 有返回值
            self.__login_time(data[0])  # 修改用户上线时间
            return data
        else:
            return False



