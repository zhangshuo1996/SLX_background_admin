from web_admin.dao import user_dao
from web_admin.utils import encrypt
import re


def check_user(username, password):
    """
    根据账户名密码
    :param username:用户名（str）
    :param password: 原始密码（str）
    :return:  字典对象{'ID': 1, 'NAME': '测试账号', 'TYPE': '1'}
            or None
    """
    tel = re.compile(r"^\d{11}$")
    email = re.compile(r"^[\w\d]+@[\w\d]+\.com$")
    u_id = re.compile(r"^\d{6,8}$")
    #  加密出密码
    password = encrypt.encryption(password)
    back = None

    # 利用正则判断用户名是否符合标准，以减少 sql 注入可能性
    if tel.match(username):
        # 以电话登陆
        back = user_dao.do_login(telephone=username, pwd=password)
    elif email.match(username):
        # 以邮件登陆
        back = user_dao.do_login(email=username, pwd=password)
    else:
        # 以 用户名登陆
        back = user_dao.do_login(name=username, pwd=password)

    # 返回查询结果
    return back

if __name__ == "__main__":
    #测试登录
    s = check_user('zhang','a')
    # print(s)
