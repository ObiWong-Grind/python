"""
    响应处理
"""


class HandleResponse:
    """
        响应处理工具类
    """
    @staticmethod
    def handle_history_id(response_head):
        """
            提取响应头中的历史记录详情信息
        :param response_head: 响应头
        :return: option_key,request,o_diagram,f_diagram,s_diagram,t_diagram,request_time
        """
        response = response_head.split("\n")
        option_key = response[0].split("Option_Key: ")[1]
        request = response[1].split("Request: ")[1]
        o_diagram = response[2].split("O_Diagram: ")[1]
        f_diagram = response[3].split("F_Diagram: ")[1]
        s_diagram = response[4].split("S_Diagram: ")[1]
        t_diagram = response[5].split("T_Diagram: ")[1]
        request_time = response[6].split("Request_Time: ")[1]
        return option_key, request, o_diagram, f_diagram, s_diagram, t_diagram, request_time

    @staticmethod
    def handle_history(msg):
        """
            提取信息中的每一条历史记录
        :param msg: 信息
        :return: 生成器函数
        """
        tmp = msg.split("FTP/1.0 200 OK\r\n")
        for item in tmp:
            t = item.split("\r\n")
            if t[0]:
                t2 = t[0].split("\n")
                id_ = t2[0].split("Id: ")[1]
                user_name = t2[1].split("User_Name: ")[1]
                option_key = t2[2].split("Option_Key: ")[1]
                request = t2[3].split("Request: ")[1]
                request_time = t2[4].split("Request_Time: ")[1]
                yield id_, user_name, option_key, request, request_time

    @staticmethod
    def handle_diagrams(response_head):
        """
            提取响应头的四个卦体
        :param response_head: 响应头
        :return: 原卦, 本卦, 互卦, 变卦
        """
        response = response_head.split("\n")
        o_diagram = response[0].split(" ")[1]
        f_diagram = response[1].split(" ")[1]
        s_diagram = response[2].split(" ")[1]
        t_diagram = response[3].split(" ")[1]
        return o_diagram, f_diagram, s_diagram, t_diagram

    @staticmethod
    def handle_id_and_name(response_head):
        """
            提取响应头中的用户id和昵称
        :param response_head: 响应头
        :return: 用户id, 用户昵称
        """
        response = response_head.split("\n")
        user_id = response[0].split(" ")[1]
        user_name = response[1].split(" ")[1]
        return user_id, user_name

    @staticmethod
    def handle_response_info(response_data):
        """
            处理响应
        :param response_data: 响应内容
        :return: 响应码, 响应信息，响应头
        """
        response = response_data.split("\r\n")
        response_row = response[0].split(" ")
        response_code = response_row[1]
        response_info = response_row[2]
        if not response[1]:
            response_head = None
        else:
            response_head = response[1]
        return response_code, response_info, response_head



