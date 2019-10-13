"""
    请求处理
"""


class HandleRequest:
    """
        请求处理工具类
    """
    @staticmethod
    def handle_request(request_head):
        """
            处理求卦请求
        :param request_head: 请求头
        :return:
        """
        request = request_head.split("\n")
        user_id = request[0].lstrip("User_Id: ")
        user_name = request[1].lstrip("User_Name: ")
        option_key = request[2].lstrip("Option_Key: ")
        if option_key == "1":
            number_one = None
            number_two = None
            return user_id, user_name, option_key, number_one, number_two
        elif option_key == "2":
            number_one = request[3].lstrip("Number_One: ")
            number_two = request[4].lstrip("Number_Two: ")
            return user_id, user_name, option_key, number_one, number_two

    @staticmethod
    def handle_insert(request_head):
        """
            处理注册时用户信息录入请求
        :param request_head: 请求头
        :return: phone 账户手机号 str; password 密码 str; user_name 用户昵称 str
        """
        request = request_head.split("\n")
        phone = request[0].lstrip("Phone: ")
        password = request[1].lstrip("Password: ")
        user_name = request[2].lstrip("User_Name: ")
        return phone, password, user_name

    @staticmethod
    def handle_sign(request_head):
        """
            处理注册请求
        :param request_head: 注册请求头
        :return: phone 账户手机号 str
        """
        return request_head.lstrip("Phone: ")

    @staticmethod
    def handle_login(request_head):
        """
            处理登录请求
        :param request_head: 登录请求头
        :return: account 手机格式的账户 str; password 密码 str
        """
        request = request_head.split("\n")
        account = request[0].lstrip("Account: ")
        password = request[1].lstrip("Password: ")
        return account, password

    @staticmethod
    def handle_request_info(request_data):
        """
            处理请求内容，根据请求行做相应的处理
        :param request_data: 请求内容
        :return: 请求头关键字, [请求行, 请求体]
        """
        request = request_data.split("\r\n")  # 按切割请求
        request_row = request[0].split(" ")
        if request_row[0] == "LOGIN":
            return request_row[0], request[1], None
        elif request_row[0] == "SIGN":
            return request_row[0], request[1], None
        elif request_row[0] == "INSERT":
            return request_row[0], request[1], None
        elif request_row[0] == "REQUEST":
            return request_row[0], request[1], request[3]
        elif request_row[0] == "HISTORY":
            pass
        elif request_row[0] == "EXIT":
            return request_row[0], None, None






