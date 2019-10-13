"""
    服务端链接模块
"""


import signal, time
from socket import *
from server_process.diagrams_ui import *


HOST = "0.0.0.0"
PORT = 38597
ADDR = (HOST, PORT)


class DiagramsSocket:
    """
        服务端网络模型
    """
    def __init__(self):
        """
            初始化TCP套接字
        """
        self._sockfd = socket()  # 创建tcp套接字
        self._sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)  # 设置套接字端口立即重用
        self._sockfd.bind(ADDR)  # 绑定地址
        self._sockfd.listen(10)  # 设置监听
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)  # 设置处理僵尸进程

    def __write_log(self, text):
        """
            记录错误日志
        :param text: 错误日志文本
        """
        str_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 将时间元组 --> str
        log = "%s | %s\n" % (str_time, text)
        with open("log.txt", "a+") as f:
            f.write(log)

    def __found_process(self):
        """
            主进程循环接收客户端连接，产生子进程
        """
        while True:
            try:
                connfd, addr = self._sockfd.accept()  # 阻塞等待客户端链接
                print("Connect from", addr)
            except KeyboardInterrupt:  # 当服务器退出
                sys.exit("Server Exit...")  # 关闭主进程
            except Exception as e:  # 其余错误记录日志
                self.__write_log(e)
                continue

            client = DiagramsView(connfd, addr)
            client.daemon = True
            client.start()

    def main(self):
        """
            入口
        """
        self.__found_process()

