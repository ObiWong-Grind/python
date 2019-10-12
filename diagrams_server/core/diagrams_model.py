"""
    定义数据模型
"""


class YaoModel:
    """
        爻
    """
    def __init__(self):
        """
            1代表阳爻, 2代表阴爻, 3代表阳爻动, 4代表阴爻动
        """
        self.__yang_yao = "1"
        self.__yin_yao = "2"
        self.__yang_change = "3"
        self.__yin_change = "4"

    @property
    def yang_yao(self):
        return self.__yang_yao

    @property
    def yin_yao(self):
        return self.__yin_yao

    @property
    def yang_change(self):
        return self.__yang_change

    @property
    def yin_change(self):
        return self.__yin_change

    def generate_diagram(self):
        raise NotImplementedError()


class QianDiagram(YaoModel):
    """
        乾卦 1, 1, 1
    """
    def __init__(self):
        super().__init__()

    def generate_diagram(self):
        diagrams_list = [self.yang_yao, self.yang_yao, self.yang_yao]
        return diagrams_list


class DuiDiagram(YaoModel):
    """
        兑卦 2, 1, 1
    """
    def __init__(self):
        super().__init__()

    def generate_diagram(self):
        diagrams_list = [self.yin_yao, self.yang_yao, self.yang_yao]
        return diagrams_list


class LiDiagram(YaoModel):
    """
        离卦 1, 2, 1
    """
    def __init__(self):
        super().__init__()

    def generate_diagram(self):
        diagrams_list = [self.yang_yao, self.yin_yao, self.yang_yao]
        return diagrams_list


class ZhenDiagram(YaoModel):
    """
        震卦 2, 2, 1
    """
    def __init__(self):
        super().__init__()

    def generate_diagram(self):
        diagrams_list = [self.yin_yao, self.yin_yao, self.yang_yao]
        return diagrams_list


class XunDiagram(YaoModel):
    """
        巽卦 1, 1, 2
    """
    def __init__(self):
        super().__init__()

    def generate_diagram(self):
        diagrams_list = [self.yang_yao, self.yang_yao, self.yin_yao]
        return diagrams_list


class KanDiagram(YaoModel):
    """
        坎卦 2, 1, 2
    """
    def __init__(self):
        super().__init__()

    def generate_diagram(self):
        diagrams_list = [self.yin_yao, self.yang_yao, self.yin_yao]
        return diagrams_list


class GenDiagram(YaoModel):
    """
        艮卦 1, 2, 2
    """
    def __init__(self):
        super().__init__()

    def generate_diagram(self):
        diagrams_list = [self.yang_yao, self.yin_yao, self.yin_yao]
        return diagrams_list


class KunDiagram(YaoModel):
    """
        坤卦 2, 2, 2
    """
    def __init__(self):
        super().__init__()

    def generate_diagram(self):
        diagrams_list = [self.yin_yao, self.yin_yao, self.yin_yao]
        return diagrams_list








