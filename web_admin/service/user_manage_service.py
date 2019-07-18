from web_admin.utils.mongo_operator import MongoOperator
from web_admin.config import MongoDB_CONFIG


mongo = MongoOperator(**MongoDB_CONFIG)


def get_user():
    """
    获取所有活跃的用户信息
    :return: user:所有用户的信息
    """
    mongo_operator = MongoOperator(**MongoDB_CONFIG)
    user_set = mongo_operator.get_collection("user")
    user = user_set.find({"status": '1'})
    user_list = []
    for i in user:
        try:
            if 'charge_school' in i:
                str = i['charge_school'][0]
                for j in i['charge_school'][1:]:
                    str = str+","+j
                user_list.append([i['name'],i['tel_number'],i['email'],str,i['id'],i['type'],i['id']])
            else:
                user_list.append([i['name'], i['tel_number'], i['email'],'',i['id'],i['type'],i['id']])
        except BaseException:
            pass
    return user_list

def add_user(user_dict):
    """
    将新建用户的信息入库
    :param user_dict:
    :return:
    """
    mongo_operator = MongoOperator(**MongoDB_CONFIG)
    user = mongo_operator.get_collection("user")
    user.insert_one(user_dict)

def delete_user(user_id):
    """
    根据user_id(用户id),将用户的状态修改为0
    :param :user_id:用户id
    :return:
    """
    mongo_operator = MongoOperator(**MongoDB_CONFIG)
    user = mongo_operator.get_collection("user")
    user.update_many({"id":user_id},{"$set":{"status":"0"}})

def update_user(user_dict):
    """
    根据用户id修改用户的信息
    :param user_dict:用户的信息（用户id,用户名，联系电话，邮箱，所在学校，用户类型）
    :return:
    """
    mongo_operator = MongoOperator(**MongoDB_CONFIG)
    user = mongo_operator.get_collection("user")
    user.update_many({"id": user_dict['id']}, {"$set": {"name":user_dict['name'],"tel_number":user_dict['tel_number'],
                                            "email":user_dict['email'],"type":user_dict['type'],"charge_school":user_dict['charge_school']}})



if __name__ == "__main__":
    #测试

    # add_user(user)
    user = {'id': 100006, 'tel_number': '12345678905', 'type': '0', 'name': '李永杰', 'email': 'e@m.com', 'charge_school': ['清华大学']}
    update_user(user)
