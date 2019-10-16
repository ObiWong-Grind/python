"""
    登录模块
"""


from core.operation_db import *


class DiagramLogin:
    """
        登录模块
    """
    def __init__(self):
        """
            初始化
        """
        self.__connect_db = OperationDB()

    def select_login_info(self, account, password):
        """
            使用账号、密码通过sql语句执行 匹配账号密码是否正确
        """
        return self.__connect_db.select_login_info(account, password)



