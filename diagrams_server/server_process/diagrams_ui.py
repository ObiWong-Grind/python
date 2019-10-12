"""
    ui

    把这个模块重构为和客户端交互的入口

    {
            "本卦": "%s" % f_diagram,
            "互卦": "%s" % s_diagram,
            "变卦": "%s" % t_diagram,
        }
"""

import random, sys, re
from core.diagrams_bll import *
from multiprocessing import Process
from login_and_sign.sign import *


class DiagramsView(Process):
    """
        起卦视图
    """
    count = 0

    def __init__(self, connfd, addr):
        """
            初始化
        :param connfd: 连接套接字
        :param addr: 连接地址
        """
        self._connfd = connfd
        self._addr = addr
        self._login = DiagramLogin()
        super().__init__()

    def __random_diagrams(self, user_id, user_name, option_key, request):
        """
            随机数起卦
        :param user_id: 用户id
        :param user_name: 用户昵称
        :param option_key: 键值
        :param request: 求问问题
        """
        tuple_result = DiagramsController(random.randint(0, 100), random.randint(0, 100), user_id, user_name, option_key, request).output()
        self._connfd.send(tuple_result.encode())

    def __choice_number_diagrams(self, number01, number02, user_id, user_name, option_key, request):
        """
            报数起卦
        """
        tuple_result = DiagramsController(number01, number02, user_id, user_name, option_key, request).output()
        self._connfd.send(tuple_result.encode())

    def __handle_diagrams_request(self, msg):
        """
            处理卦的请
        :param msg: 请求信息
        """
        pattern = r"(\S+)##--##(\S+)##--##(\S+)##--##(\S+)##--##(\S+)##--##(\S+)"
        user_id, user_name, option_key, number01, number02, request = re.findall(pattern, msg)[0]
        if option_key == "1":
            number01 = number02 = None
            self.__random_diagrams(int(user_id), user_name, option_key, request)
        elif option_key == "2":
            self.__choice_number_diagrams(int(number01), int(number02), int(user_id), user_name, option_key, request)

    def __select_sign(self, msg):
        """
            完成注册，将新用户信息插入数据库
        :param msg:
        """
        pattern = r"(\S+),(\S+),(\S+)"
        phone, password, user_name_ = re.findall(pattern, msg)[0]
        result = DiagramSign(phone)
        res = result.insert_user(password, user_name_)
        if res:
            msg = "FTP/1.0 200 OK#%s#%s" % (res[0], res[1])
            self._connfd.send(msg.encode())
        else:
            self._connfd.send(b"FTP/1.0 403 ERROR")

    def __do_process_exit(self):
        """
            相关用户退出服务
        """
        self._connfd.close()
        sys.exit("%s, %s Exit Handler" % self._addr)

    def __do_sign(self, phone):
        """
            验证手机号是否被注册
        :param phone: 手机号
        """
        result = DiagramSign(phone).select_phone()
        if result:
            self._connfd.send(b"FTP/1.0 200 OK")
        else:
            self._connfd.send(b"FTP/1.0 402 HAVE_PHONE")

    def __do_login(self, msg):
        """
            登录
        :param msg: 提取出的信息
        """
        pattern = r"(\S+),(\S+)"
        account, password = re.findall(pattern, msg)[0]
        result = self._login.match_login_info(account, password)
        if result:
            msg = "FTP/1.0 200 OK#%s#%s" % (result[0], result[1])
            self._connfd.send(msg.encode())
        else:
            self._connfd.send(b"FTP/1.0 401 ACCOUNT_OR_PASSWD_ERROR")

    def run(self):
        """
            循环接收请求，按照协议内容执行相应方法
        """
        while True:
            request_data = self._connfd.recv(4096).decode()  # 阻塞等待请求
            request = request_data.split(" ")  # 按切割请求
            if not request or request[0] == "EXIT":
                self.__do_process_exit()
            elif request[0] == "LOGIN":  # 当用户请求登录时
                msg = request[1].lstrip("/")
                self.__do_login(msg)
            elif request[0] == "SIGN":  # 当用户请求注册时
                phone = request[1].lstrip("/")
                self.__do_sign(phone)
            elif request[0] == "SELECT":  # 完成注册插入新的用户数据
                msg = request[1].lstrip("/")
                self.__select_sign(msg)
            elif request[0] == "REQUEST":  # 当用户请求请卦时
                msg = request[1].lstrip("/")
                self.__handle_diagrams_request(msg)
            elif request[0] == "HISTORY":  # 当用户请求历史记录时
                pass






