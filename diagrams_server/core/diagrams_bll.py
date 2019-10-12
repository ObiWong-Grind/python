"""
    Python 以面向对象的方式做梅花排卦核心, 纯粹是个人练习
"""

import pymysql
from core.diagrams_model import *


class DiagramsController:
    """
        卦爻划分
    """
    def __init__(self, number01, number02, user_id, user_name, option_key, request):
        self.__yao = YaoModel()
        self.__number_one = number01
        self.__number_two = number02
        self.__user_id = user_id
        self.__user_name = user_name
        self.__option_key = option_key
        self.__request = request
        self.__connect_db()
        self.__o_diagram = ""

    def __connect_db(self):
        """
            链接数据库
        """
        self.db = pymysql.connect(host="localhost", port=3306, user="root", password="r0260zgmf", database="diagrams", charset="utf8")
        self.cur = self.db.cursor()

    def __record_original_diagram(self, target_list):
        """
            记录原本卦
        :param target_list: 卦列表
        """
        self.__o_diagram = "".join(target_list)

    def __generate_total_diagram(self):
        """
            生成本卦动爻数字
        :return: change_number 动爻数, diagram_list 本卦
        """
        change_number = self.__change_remainder(self.__number_one + self.__number_two)
        diagram_list = self.__generate_yaos(self.__get_remainder(self.__number_one)) + self.__generate_yaos(self.__get_remainder(self.__number_two))
        return change_number, diagram_list

    def __get_remainder(self, value):
        """
            给整数取8的余数
        :param value: int型
        :return: 0-7 int型
        """
        return value % 8

    def __change_remainder(self, value):
        """
            给整数取6的余数
        :param value: int型
        :return: 0-5 int型
        """
        return value % 6

    def __generate_yaos(self, value):
        """
            排出一个自上而下的三爻的卦
            六爻卦索引[0, 1, 2, 3, 4, 5] 等同于 ["六爻", "五爻", "四爻", "三爻", "二爻", "一爻"]
        :param value: 排三爻卦所需值
        """
        if value == 1:
            return QianDiagram().generate_diagram()
        elif value == 2:
            return DuiDiagram().generate_diagram()
        elif value == 3:
            return LiDiagram().generate_diagram()
        elif value == 4:
            return ZhenDiagram().generate_diagram()
        elif value == 5:
            return XunDiagram().generate_diagram()
        elif value == 6:
            return KanDiagram().generate_diagram()
        elif value == 7:
            return GenDiagram().generate_diagram()
        elif value == 0:
            return KunDiagram().generate_diagram()

    def __change_rule(self, number, target_list, function):
        """
            本卦、变卦相关变爻的变化规则
            函数式编程
        """
        if number == 1:
            function(target_list, 5)
        elif number == 2:
            function(target_list, 4)
        elif number == 3:
            function(target_list, 3)
        elif number == 4:
            function(target_list, 2)
        elif number == 5:
            function(target_list, 1)
        elif number == 0:
            function(target_list, 0)

    def __first_diagram(self):
        """
            生成本卦变爻标记的本卦
        :return: 六个元素的本卦列表
        """
        change_yao_number, result_list = self.__generate_total_diagram()
        self.__record_original_diagram(result_list)
        self.__change_rule(change_yao_number, result_list, self.__first_change)
        return result_list

    def __first_change(self, target_list, indexes):
        """
            替换本卦中的变爻
        """
        if target_list[indexes] == "1":
            target_list[indexes] = self.__yao.yang_change
        else:
            target_list[indexes] = self.__yao.yin_change

    def __second_diagram(self):
        """
            生成互卦
        :return: 六个元素的互卦列表
        """
        re = self.__generate_total_diagram()
        result_list = re[1]
        result_list = result_list[1:4] + result_list[2:5]
        return result_list

    def __third_diagram(self):
        """
            生成变卦
        :return: 六个元素的本卦列表
        """
        change_yao_number, result_list = self.__generate_total_diagram()
        self.__change_rule(change_yao_number, result_list, self.__third_change)
        return result_list

    def __third_change(self, target_list, indexes):
        """
            在变卦中替换变爻
        """
        if target_list[indexes] == "1":
            target_list[indexes] = self.__yao.yin_yao
        else:
            target_list[indexes] = self.__yao.yang_yao

    def __insert_sql(self, f_diagram, s_diagram, t_diagram):
        """
            插入数据库
        :param f_diagram: 本卦
        :param s_diagram: 互卦
        :param t_diagram: 变卦
        """
        try:
            sql = "insert into three_diagrams (user_id,user_name,option_key,request,o_diagram,f_diagram,s_diagram,t_diagram) values (%s,%s,%s,%s,%s,%s,%s,%s);"
            self.cur.execute(sql, [self.__user_id, self.__user_name, self.__option_key, self.__request, self.__o_diagram, f_diagram, s_diagram, t_diagram])
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
        finally:
            self.cur.close()
            self.db.close()

    def output(self):
        f_diagram = "".join(self.__first_diagram())
        s_diagram = "".join(self.__second_diagram())
        t_diagram = "".join(self.__third_diagram())
        self.__insert_sql(f_diagram, s_diagram, t_diagram)
        return self.__o_diagram, f_diagram, s_diagram, t_diagram



