"""
请求协议
    登录: "LOGIN / FTP/1.0",
    注册: "SIGN / FTP/1.0",
    完成注册: "SELECT / FTP/1.0",
    求卦: "REQUEST / FTP/1.0"
    历史记录: "HISTORY / FTP/1.0"

    完整求情协议: "请求 / FTP/1.0\r\nUser_Id:1\nUser_Name:xxxxx\nOption_Key:2\nNumber_One:20\nNumber_Two:20\r\n\r\n请求内容"

响应协议
    响应成功: "FTP/1.0 200 OK",

    完整响应协议 'FTP/1.0 200 OK\r\nUser_Id:1\nUser_Name:xxxxx\r\n\r\n请求内容'
"""

import sys, getpass
from tools.handle_response import *
from client_common.config import *

MENU_1 = """
========= 导航命令 =========
        1. 登录
        2. 注册
        Q. 关闭
===========================
"""

MENU_2 = """
=========== 命令 ===========
        1. 起卦
        2. 历史记录
        3. 退出
===========================
"""

MENU_3 = """
=========== 命令 ===========
        1. 随机起卦
        2. 报数起卦
        3. 返回上级
===========================
"""

MENU_4 = """
=========== 命令 ===========
    输入 id编号 查看历史详情
     输入 exit 返回上一级
===========================
"""

yang_yao = "---"
yin_yao = "- -"
yang_change = "--- o"
yin_change = "- - x"


class DiagramsClientView:
    """
        FTP客户端视图
    """
    count = 0

    def __init__(self, sockfd):
        """
            初始化
        :param sockfd: 套接字
        """
        self.__sockfd = sockfd
        self.__tools = HandleResponse()
        self.__user_id = None
        self.__user_name = None
        self.__o_diagram = ""
        self.__f_diagram = ""
        self.__s_diagram = ""
        self.__t_diagram = ""
        self.__hist_id_list = []

    def __create_dict(self):
        """
            生成字典
        """
        diagrams_dict = {
            "本卦": "%s" % self.__f_diagram,
            "互卦": "%s" % self.__s_diagram,
            "变卦": "%s" % self.__t_diagram,
        }
        self.__show_dict(diagrams_dict)

    def __show_dict(self, target_dict):
        """
            输出字典
        :param target_dict: 字典
        """
        for key, value in target_dict.items():
            self.__replace_show(key, value)

    def __replace_show(self, str_var, target_list):
        """
            将列表中的数值转行符号一一打印在控制台中
        :param str_var: 本卦 互卦 变卦 str
        :param target_list: 传输一个六爻的列表
        """
        print()
        print(str_var)
        for item in target_list:
            if item == "1":
                print(yang_yao)
            elif item == "2":
                print(yin_yao)
            elif item == "3":
                print(yang_change)
            elif item == "4":
                print(yin_change)

    def __do_exit(self):
        """
            退出进程
            由于客户端是一个单独的进程所以可以用sys.exit()结束进程
        """
        self.__sockfd.send("EXIT / FTP/1.0".encode())
        self.__sockfd.close()
        sys.exit("欢迎下次再来！")

    def __random_diagrams(self, option_key):
        """
            随机数起卦
        """
        request = input("请输入您的求问内容：")
        request_data = "REQUEST / FTP/1.0\r\nUser_Id: %s\nUser_Name: %s\nOption_Key: %s\r\n\r\n%s" % (self.__user_id, self.__user_name, option_key, request)
        self.__sockfd.send(request_data.encode())
        response = self.__sockfd.recv(512).decode()
        response_code, response_info, response_head = self.__tools.handle_response_info(response)
        if response_code == "100" and response_info == "FOUR_DIAGRAMS":
            self.__o_diagram, self.__f_diagram, self.__s_diagram, self.__t_diagram = self.__tools.handle_diagrams(response_head)
            self.__create_dict()

    def __choice_number_diagrams(self, option_key):
        """
            报数起卦
        """
        request = input("请输入您的求问内容：")
        number01 = self.__input_number()
        number02 = self.__input_number()
        request_data = "REQUEST / FTP/1.0\r\nUser_Id: %s\nUser_Name: %s\nOption_Key: %s\nNumber_One: %s\nNumber_Two: %s\r\n\r\n%s" % (self.__user_id, self.__user_name, option_key, number01, number02, request)
        self.__sockfd.send(request_data.encode())
        response = self.__sockfd.recv(512).decode()
        response_code, response_info, response_head = self.__tools.handle_response_info(response)
        if response_code == "100" and response_info == "FOUR_DIAGRAMS":
            self.__o_diagram, self.__f_diagram, self.__s_diagram, self.__t_diagram = self.__tools.handle_diagrams(response_head)
            self.__create_dict()

    def __input_number(self):
        """
            输入的数值
        """
        DiagramsClientView.count += 1
        number = self.__input_number_error()
        return number

    def __input_number_error(self):
        """
            判断数字输入是否符合要求
        """
        while True:
            number = input("请您输入第%d个0-50的数字：" % DiagramsClientView.count)
            try:
                number = int(number)
                if number < 0 or number > 50:
                    raise ValueError("请输入要求范围内的数字！")
            except Exception as e:
                print(e)
                continue
            return number

    def __request_diagram(self):
        """
            求挂
        """
        while True:
            print(MENU_3)
            try:
                cmd = input("输入命令请选择起卦方式：")
            except KeyboardInterrupt:
                sys.exit("欢迎下次再来！")
            if cmd.strip() == "1":
                self.__random_diagrams(cmd.strip())
            elif cmd.strip() == "2":
                self.__choice_number_diagrams(cmd.strip())
            elif cmd.strip() == "3":
                return
            else:
                print("输入的命令不正确！")

    def __history_id(self):
        """
            输入历史记录编号
        """
        while True:
            print(MENU_4)
            try:
                id_number = input("请输入ID：")
            except KeyboardInterrupt:
                sys.exit("欢迎下次再来！")
            if id_number == "exit" or id_number == "Exit":
                return
            if id_number not in self.__hist_id_list:
                print("请输入正确ID！")
                continue
            self.__request_hist_id(id_number)

    def __request_hist_id(self, id_number):
        """
            按编号请求查看历史记录详情
        :param id_number: 历史记录id
        """
        request_data = "HISTORY_ID / FTP/1.0\r\nHist_Id: %s\nUser_Name: %s\r\n\r\n" % (id_number, self.__user_name)
        self.__sockfd.send(request_data.encode())
        response = self.__sockfd.recv(512).decode()
        response_code, response_info, response_head = self.__tools.handle_response_info(response)
        if response_code == "200" and response_info == "OK":
            option_key, request, self.__o_diagram, self.__f_diagram, self.__s_diagram, self.__t_diagram, request_time = self.__tools.handle_history_id(response_head)
            print("求卦内容：", request)
            if option_key == "1":
                print("求卦方式：", "随机起卦")
            elif option_key == "2":
                print("求卦方式：", "报数起卦")
            print("求卦时间：", request_time)
            self.__create_dict()
        elif response_code == "404" and response_info == "FAIL":
            print("未找到该条历史记录！")
            return

    def __history(self):
        """
            查看历史
        """
        request_data = "HISTORY / FTP/1.0\r\nUser_Id: %s\nUser_Name: %s\r\n\r\n" % (self.__user_id, self.__user_name)
        self.__sockfd.send(request_data.encode())
        response = self.__sockfd.recv(4096).decode()
        response_code, response_info, response_head, response_body = self.__tools.handle_response_all(response)
        if response_code == "200" and response_info == "OK":  # 有历史记录
            self.__print_hist(response_body)
            self.__history_id()
        else:
            print("没有历史记录！")
            return

    def __print_hist(self, msg):
        """
            打印历史记录
        :param msg: 接收到的历史记录信息
        """
        for item in self.__tools.handle_history(msg):
            option_key = ""
            if item[2] == "1":
                option_key = "随机起卦"
            elif item[2] == "2":
                option_key = "报数起卦"
            print("id:%s | %s | %s | %s | %s" % (item[0], item[1], option_key, item[4], item[3]))
            if item[0] not in self.__hist_id_list:
                self.__hist_id_list.append(item[0])

    def __do_play(self):
        """
            选择起卦、历史记录、退出
        """
        while True:
            print(MENU_2)
            try:
                cmd = input("输入命令请选择服务：")
            except KeyboardInterrupt:
                sys.exit("欢迎下次再来！")
            if cmd.strip() == "1":
                self.__request_diagram()
            elif cmd.strip() == "2":
                self.__history()
            elif cmd.strip() == "3":
                self.input_cmd()
            else:
                print("输入的命令不正确！")

    def __input_user_name(self):
        """
            输入昵称
            后续加验证
        """
        while True:
            user_name = input("请输入昵称：")
            if " " in user_name or " " in user_name:
                print("你输入的昵称中存在不符合规定的内容，请重新输入！")
                continue
            return user_name

    def __input_password(self):
        """
            输入密码
            后续要做加格式验证
        """
        while True:
            pwd = getpass.getpass("请输入密码：")
            if " " in pwd or " " in pwd:
                print("你输入的密码中存在不符合规定的内容，请重新输入！")
            else:
                return pwd

    def __input_phone(self, msg):
        """
            输入手机号账号
        :param msg: 提示信息
        :return: 手机号
        """
        while True:
            phone = input(msg)
            if " " in phone or " " in phone:
                print("你输入的手机号中存在不符合规定的内容，请重新输入！")
            elif not phone.isdigit() or len(phone) != 11:
                print("你输入的手机号格式有误，请重新输入！")
            elif phone[0:3] not in phone_number_head:
                print("输入的手机号格式有误，目前仅支持大路地区用户！")
            else:
                return phone

    def __over_sign(self, phone):
        """
            手机通过验证后，完成注册流程
        :param phone: 手机
        """
        password = self.__input_password()
        user_name = self.__input_user_name()
        request_data = "INSERT / FTP/1.0\r\nPhone: %s\nPassword: %s\nUser_Name: %s\r\n\r\n" % (phone, password, user_name)
        self.__sockfd.send(request_data.encode())
        response = self.__sockfd.recv(512).decode()
        response_code, response_info, response_head = self.__tools.handle_response_info(response)
        if response_code == "200" and response_info == "OK":  # 注册成功
            print("注册成功！")
            self.__extract(response_head)  # 提取返回的用户id和昵称
            self.__do_play()
        else:
            print("未知异常！")
            return

    def __do_sign(self):
        """
            注册流程
        """
        while True:
            phone = self.__input_phone("请输入手机号：")
            request_data = "SIGN / FTP/1.0\r\nPhone: %s\r\n\r\n" % phone
            self.__sockfd.send(request_data.encode())
            response = self.__sockfd.recv(512).decode()
            response_code, response_info, response_head = self.__tools.handle_response_info(response)
            if response_code == "200" and response_info == "OK":  # 如果返回 200 和 OK 手机未注册
                self.__over_sign(phone)
            elif response_code == "402" and response_info == "HAVE_PHONE":
                print("该手机号已被注册！")

    def __extract(self, response_head):
        """
            提取用户id及昵称
        :param response_head:
        :return: id, 用户名
        """
        self.__user_id, self.__user_name = self.__tools.handle_id_and_name(response_head)

    def __do_login(self):
        """
            输入账号、密码，进行登录流程
        """
        while True:
            account = self.__input_phone("请输入账号：")
            password = self.__input_password()
            request_data = "LOGIN / FTP/1.0\r\nAccount: %s\nPassword: %s\r\n\r\n" % (account, password)
            self.__sockfd.send(request_data.encode())
            response = self.__sockfd.recv(512).decode()
            response_code, response_info, response_head = self.__tools.handle_response_info(response)
            if response_code == "200" and response_info == "OK":  # 如果返回 200 账号密码正确
                print("登录成功！")
                self.__extract(response_head)
                self.__do_play()
            elif response_code == "401" and response_info == "ACCOUNT_OR_PASSWD_ERROR":
                print("账号或密码有误，请重新输入！")

    def input_cmd(self):
        """
            输入选项
        """
        while True:
            print(MENU_1)
            try:
                cmd = input("输入命令选择登录/注册：")
            except KeyboardInterrupt:
                sys.exit("欢迎下次再来！")
            if cmd.strip() == "1":
                self.__do_login()
            elif cmd.strip() == "2":
                self.__do_sign()
            elif cmd.strip() == "Q" or cmd.strip() == "q":
                self.__do_exit()
            else:
                print("输入的命令不正确！")


