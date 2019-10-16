"""
    注册模块
"""


from login_and_sign.login import *
from core.operation_db import *


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
        self.__connect_db = OperationDB()

    def insert_user(self, password, user_name):
        """
            验证通过，往数据库插入新的用户数据
        :param password: 密码
        :param user_name: 用户名
        """
        return self.__connect_db.insert_user(self._phone, password, user_name)

    def select_phone(self):
        """
            查询注册账户是否在
        :return: False 手机号被占用，True 未被占用
        """
        return self.__connect_db.select_phone(self._phone)

