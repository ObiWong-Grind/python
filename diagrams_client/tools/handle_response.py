"""
    响应处理
"""


class HandleResponse:
    @staticmethod
    def handle_diagrams(response_head):
        """
            提取响应头的四个卦体
        :param response_head: 响应头
        :return: 原卦, 本卦, 互卦, 变卦
        """
        response = response_head.split("\n")
        o_diagram = response[0].lstrip("O_Diagram: ")
        f_diagram = response[1].lstrip("F_Diagram: ")
        s_diagram = response[2].lstrip("S_Diagram: ")
        t_diagram = response[3].lstrip("T_Diagram: ")
        return o_diagram, f_diagram, s_diagram, t_diagram

    @staticmethod
    def handle_id_and_name(response_head):
        """
            提取响应头中的用户id和昵称
        :param response_head: 响应头
        :return: 用户id, 用户昵称
        """
        response = response_head.split("\n")
        user_id = response[0].lstrip("User_Id: ")
        user_name = response[1].lstrip("User_Name: ")
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



