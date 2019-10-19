"""
    客户端套接字
"""


from socket import *
from client_core.diagrams_client_ui import *
from client_common.config import *


ADDR = (HOST, PORT)


class DiagramClient:
    """
        客户端网络模型
    """
    def __init__(self):
        """
            初始化创建客户端套接字
        """
        self.__sockfd = socket()

    def __link_server(self):
        """
            创建tcp连接
        """
        try:
            self.__sockfd.connect(ADDR)
        except Exception as e:
            print(e)
            return

        ftp = DiagramsClientView(self.__sockfd)
        ftp.input_cmd()

    def main(self):
        """
            入口
        """
        self.__link_server()


