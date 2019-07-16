from web_admin.utils.mongo_operator import MongoOperator

mongo = MongoOperator()
user_col = mongo.get_collection("user")

def add_user(user_dict):
    """
    将新建用户的信息入库
    :param user_dict:
    :return:
    """

    # TODO 处理user_dict

    user_col.insert_one(user_dict)


def delete_user(user_id):
    """
    根据user_id,删除对应的用户信息
    :param user_id:
    :return:
    """

    # TODO
    user_col.delete_one({"id": user_id})


def update_user(update_dict):
    """
    根据update_dict更新对应的用户信息
    :param update_dict:
    :return:
    """
