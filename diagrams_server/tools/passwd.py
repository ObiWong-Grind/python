"""
    密码加密模块
"""


import hashlib


class PassWordHash:
    @staticmethod
    def hashpasswd(account, password):
        """
            生成加密后的密码
        :return: 加密密码
        """
        salt = account + "*#06l_"
        hash = hashlib.md5(salt.encode())  # 生成对象 ()内是盐的部分
        hash.update(password.encode())
        return hash.hexdigest()




