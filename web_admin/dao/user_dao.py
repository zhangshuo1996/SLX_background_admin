from web_admin.config import MongoDB_CONFIG
from web_admin.utils.mongo_operator import MongoOperator

def do_login(telephone=None, email=None, name=None, pwd=""):
    """
    根据 账号信息 及 密码 查询用户信息
    :param telephone: 手机号
    :param email: 邮箱
    :param name: 用户名
    :param pwd: 密码（32位字符串）
    :return: 用户信息 ： （ID,NAME）or None
    """
    # 连接服务器
    # client = pymongo.MongoClient("mongodb://" + MongoDB_CONFIG["ip"] + ":" + MongoDB_CONFIG["port"])
    mongo_operator = MongoOperator(**MongoDB_CONFIG)
    condition = {'password': pwd}

    if telephone:
        condition['tel_number'] = telephone
    elif email:
        condition['email'] = email
    elif name:
        condition['name'] = name

    result = mongo_operator.find_one(condition, 'administer')
    # 删除mongo的id
    if result:
        del result['_id']

    return result


if __name__ == "__main__":
    # 测试：
    # success with telphone
    # print(do_login(telephone="12345678901", pwd="3b86247f12fa88a116e8e446614b3eae"))
    # # success with email
    # print(do_login(email="c@m.com", pwd="3b86247f12fa88a116e8e446614b3eae"))
    # # success with user_id
    # print(do_login(u_id=100000, pwd="3b86247f12fa88a116e8e446614b3eae"))
    # # fail to login
    # print(do_login(telephone="12345678901", pwd="3b86247f12fa88a116e8e"))
    print(do_login(name='zhang',pwd='3b86247f12fa88a116e8e446614b3eae'))
