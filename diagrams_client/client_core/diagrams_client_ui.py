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

import sys
from tools.handle_response import *

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
        2. 查看历史
        Q. 关闭
===========================
"""

MENU_3 = """
=========== 命令 ===========
        1. 随机起卦
        2. 报数起卦
        3. 返回上级
===========================
"""

yang_yao = "---"
yin_yao = "- -"
yang_change = "--- o"
yin_change = "- - x"


class DiagramsClientView:
    """
        FTP客户端控制器
    """
    count = 0

    def __init__(self, sockfd):
        """
            套接字
        :param sockfd:
        """
        self.__sockfd = sockfd
        self.__tools = HandleResponse()
        self.__user_id = None
        self.__user_name = None
        self.__o_diagram = ""
        self.__f_diagram = ""
        self.__s_diagram = ""
        self.__t_diagram = ""

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
            self.__o_diagram, self.__f_diagram, self.__s_diagram, self.__t_diagram = self.__tools.handle_diagrams(
                response_head)
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
                    raise ValueError()
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
                self.__do_play()

    def __history(self):
        """
            查看历史
        """
        request_data = "HISTORY / FTP/1.0\r\nUser_Id: %s\nUser_Name: %s\r\n\r\n" % (self.__user_id, self.__user_name)
        # self.__sockfd.send(request_data.encode())

    def __do_play(self):
        """
            选择起卦、查看历史、关闭
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
            elif cmd.strip() == "Q" or cmd.strip() == "q":
                self.__do_exit()
            else:
                print("输入的命令不正确！")

    def __input_user_name(self):
        """
            输入昵称
            后续加验证
        """
        return input("请输入昵称：")

    def __input_password(self):
        """
            输入密码
            后续加验证
        """
        return input("请输入密码：")

    def __over_sign(self, phone):
        """
            手机通过验证后，完成注册流程
        :param phone: 手机
        """
        password = self.__input_password()
        user_name = self.__input_user_name()
        request_data = "SELECT / FTP/1.0\r\nPhone: %s\nPassword: %s\nUser_Name: %s\r\n\r\n" % (phone, password, user_name)
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
            phone = input("请输入手机号：")
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
            account = input("请输入账号：")
            password = input("请输入密码：")
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


