"""
2019.7.3
by zhang
"""

from web_admin.config import MongoDB_CONFIG
from web_admin.utils.mongo_operator import MongoOperator
from bson.objectid import ObjectId


def search_teacher_basic_info(teacher_id):
    """
    根据教师的id从MongoDB中获取教师的基本信息
    :param teacher_id:
    :return:
    """
    print("-------------------------开始搜索学者基本信息---------------------------------------")
    try:
        mongo_operator = MongoOperator(**MongoDB_CONFIG)
        # 指定集合
        basic_info_col = mongo_operator.get_collection("basic_info")

        basic_info_dict = basic_info_col.find_one(
            {"id": teacher_id},
            {
                "id": 1,
                "name": 1,
                "birth_year": 1,
                "title": 1,
                "email": 1,
                "school": 1,
                "institution": 1,
                "edu_exp": 1,
                "other_title": 1,
                "position": 1,
                "phone_number": 1,
                "office_number": 1
            }
        )
        # print(basic_info_dict)

    except Exception as e:
        print("------exception------  ", e)

    return basic_info_dict


def update_basic_info(basic_info_dict):
    """
    根据更改后的信息更新数据库中对应的教师基本信息
    :param basic_info_dict:
    :return:
    """
    mongo_operator = MongoOperator(**MongoDB_CONFIG)
    # 指定集合
    basic_info_col = mongo_operator.get_collection("basic_info")

    teacher_id = basic_info_dict["id"]

    info_in_mongo = basic_info_col.find_one({"id": teacher_id})
#    更新信息
    info_in_mongo["name"] = basic_info_dict["name"]
    info_in_mongo["birth_year"] = basic_info_dict["birth_year"]
    info_in_mongo["title"] = basic_info_dict["title"]
    info_in_mongo["email"] = basic_info_dict["email"]
    info_in_mongo["school"] = basic_info_dict["school"]
    info_in_mongo["edu_exp"] = basic_info_dict["edu_exp"]
    info_in_mongo["other_title"] = basic_info_dict["other_title"]
    info_in_mongo["position"] = basic_info_dict["position"]
    info_in_mongo["phone_number"] = basic_info_dict["phone_number"]
    info_in_mongo["office_number"] = basic_info_dict["office_number"]

    print(info_in_mongo)

    basic_info_col.save(info_in_mongo)






if __name__ == '__main__':
    # p = Project()
    d = {
    "_id" : ObjectId("5d1483fcde42a13dd0f56e31"),
    "email" : " ",
    "title" : "教授",
    "institution" : "马克思主义学院",
    "school" : "中国农业大学",
    "edu_exp" : "1994-1997 北京大学，获得硕士学位\n2004—2008 中国农业大学，获得博士学位",
    "name" : "王冬梅",
    "id" : 73927,
    "birth_year" : "1972",
    "other_title" : " ",
    "position" : " ",
    "patent_id" : [],
    "funds_id" : [],
    "phone_number" : " ",
    "office_number" : " ",
    "paper_id" : []
}
    # search_teacher_basic_info(73964)
    # update_basic_info(d)