"""
    ui

    把这个模块重构为和客户端交互的入口

    {
        "本卦": "%s" % f_diagram,
        "互卦": "%s" % s_diagram,
        "变卦": "%s" % t_diagram,
    }
"""

import random, sys
from core.diagrams_bll import *
from multiprocessing import Process
from tools.handle_request import *
from tools.passwd import *
from time import sleep


class DiagramsServer(Process):
    """
        起卦视图
    """
    count = 0

    def __init__(self, connfd, addr, db):
        """
            初始化
        :param connfd: 连接套接字
        :param addr: 连接地址
        :param db:
        """
        self._connfd = connfd
        self._addr = addr
        self._tools = HandleRequest()
        self._db = db  # 在父进程生成的数据库对象
        self._db.create_cursor()  # 使用这个_db对象创建属于子进程的游标
        super().__init__()

    def __random_diagrams(self, user_id, user_name, option_key, request):
        """
            随机数起卦
        :param user_id: 用户id
        :param user_name: 用户昵称
        :param option_key: 键值
        :param request: 求问问题
        """
        o_diagram, f_diagram, s_diagram, t_diagram = DiagramsController(random.randint(0, 100), random.randint(0, 100)).output()
        self._db.insert_history(user_id, user_name, option_key, request, o_diagram, f_diagram, s_diagram, t_diagram)
        msg = "FTP/1.0 100 FOUR_DIAGRAMS\r\nO_Diagram: %s\nF_Diagram: %s\nS_Diagram: %s\nT_Diagram: %s\r\n\r\n" % (o_diagram, f_diagram, s_diagram, t_diagram)
        self._connfd.send(msg.encode())

    def __choice_number_diagrams(self, number01, number02, user_id, user_name, option_key, request):
        """
            报数起卦
        :param user_id: 用户id
        :param user_name: 用户昵称
        :param option_key: 键值
        :param request: 求问问题
        """
        o_diagram, f_diagram, s_diagram, t_diagram = DiagramsController(number01, number02).output()
        self._db.insert_history(user_id, user_name, option_key, request, o_diagram, f_diagram, s_diagram, t_diagram)
        msg = "FTP/1.0 100 FOUR_DIAGRAMS\r\nO_Diagram: %s\nF_Diagram: %s\nS_Diagram: %s\nT_Diagram: %s\r\n\r\n" % (o_diagram, f_diagram, s_diagram, t_diagram)
        self._connfd.send(msg.encode())

    def __handle_diagrams_request(self, request_head, request_content):
        """
            处理请卦的请求
        :param request_head: 请求头
        :param request_content: 请求体
        """
        user_id, user_name, option_key, number_one, number_two = self._tools.handle_request(request_head)
        if option_key == "1":
            self.__random_diagrams(int(user_id), user_name, option_key, request_content)
        elif option_key == "2":
            self.__choice_number_diagrams(int(number_one), int(number_two), int(user_id), user_name, option_key, request_content)

    def __insert_new_user(self, request_head):
        """
            完成注册，将新用户信息插入数据库
        :param request_head: 请求头
        """
        phone, password, user_name = self._tools.handle_insert(request_head)
        password = PassWordHash().hash_passwd(phone, password)
        result = self._db.insert_user(phone, password, user_name)
        if result:
            msg = "FTP/1.0 200 OK\r\nUser_Id: %s\nUser_Name: %s\r\n\r\n" % (result[0], result[1])
            self._connfd.send(msg.encode())
        else:
            self._connfd.send(b"FTP/1.0 403 ERROR\r\n\r\n\r\n")

    def __do_process_exit(self):
        """
            相关用户退出服务
        """
        self._connfd.close()
        sys.exit("%s, %s Exit Handler" % self._addr)

    def __do_sign(self, request_head):
        """
            验证手机号是否被注册
        :param request_head: 请求头
        """
        phone = self._tools.handle_sign(request_head)
        result = self._db.select_phone(phone)
        if result:
            self._connfd.send(b"FTP/1.0 200 OK\r\n\r\n\r\n")
        else:
            self._connfd.send(b"FTP/1.0 402 HAVE_PHONE\r\n\r\n\r\n")

    def __do_login(self, request_head):
        """
            登录
        :param request_head: 请求头
        """
        account, password = self._tools.handle_login(request_head)
        password = PassWordHash().hash_passwd(account, password)
        result = self._db.select_login_info(account, password)
        if result:
            msg = "FTP/1.0 200 OK\r\nUser_Id: %s\nUser_Name: %s\r\n\r\n" % (result[0], result[1])
            self._connfd.send(msg.encode())
        else:
            self._connfd.send(b"FTP/1.0 401 ACCOUNT_OR_PASSWD_ERROR\r\n\r\n\r\n")

    def __handle_history(self, request_head):
        """
            处理查询历史
        :param request_head: 请求头
        """
        user_id, user_name = self._tools.handle_history(request_head)
        hist = self._db.select_history(user_id, user_name, 10)
        if not hist:
            self._connfd.send(b"FTP/1.0 404 FAIL\r\n\r\n\r\n")
            return
        msg = "FTP/1.0 200 OK\r\n\r\n\r\n"
        self._connfd.send(msg.encode())
        for item in hist:
            msg = "FTP/1.0 200 OK\r\nId: %s\nUser_Name: %s\nOption_Key: %s\nRequest: %s\nRequest_Time: %s\r\n\r\n" % (item[0], item[1], item[2], item[3], item[4])
            self._connfd.send(msg.encode())
        sleep(0.7)
        self._connfd.send(b"*#06#")

    def __handle_history_id(self, request_head):
        """
            按照id查询历史记录详情
        :param request_head: 请求头
        """
        hist_id = self._tools.handle_history_id(request_head)
        hist = self._db.select_hist_id(hist_id)
        if not hist:
            self._connfd.send(b"FTP/1.0 404 FAIL\r\n\r\n\r\n")
            return
        msg = "FTP/1.0 200 OK\r\nOption_Key: %s\nRequest: %s\nO_Diagram: %s\nF_Diagram: %s\nS_Diagram: %s\nT_Diagram: %s\nRequest_Time: %s\r\n\r\n" % (hist[0], hist[1], hist[2], hist[3], hist[4], hist[5], hist[6])
        self._connfd.send(msg.encode())

    def run(self):
        """
            循环接收请求，按照协议内容执行相应方法
        """
        while True:
            request_data = self._connfd.recv(4096).decode()  # 阻塞等待请求
            if not request_data:
                self.__do_process_exit()
            request_row, request_head, request_content = self._tools.handle_request_info(request_data)
            if request_row == "EXIT":
                self.__do_process_exit()
            elif request_row == "LOGIN":  # 当用户请求登录时
                self.__do_login(request_head)
            elif request_row == "SIGN":  # 当用户请求注册时
                self.__do_sign(request_head)
            elif request_row == "INSERT":  # 完成注册插入新的用户数据
                self.__insert_new_user(request_head)
            elif request_row == "REQUEST":  # 当用户请求请卦时
                self.__handle_diagrams_request(request_head, request_content)
            elif request_row == "HISTORY":  # 当用户请求历史记录列表时
                self.__handle_history(request_head)
            elif request_row == "HISTORY_ID":  # 用户请求历史记录ID
                self.__handle_history_id(request_head)






