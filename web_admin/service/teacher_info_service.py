"""
2019/7/22
by dxy
for teacher_info db
"""

from web_admin.utils.mongo_operator import MongoOperator
from web_admin.config import MongoDB_CONFIG


def get_modify_info():
    """
    从数据库中将商务提交的待处理的教师信息修改信息取出
    :return: agent_feedback表中所有未处理的信息
    """
    mogo_operator = MongoOperator(**MongoDB_CONFIG)
    # 从数据库中取出商务提交的所有信息
    agent_feedback = mogo_operator.get_collection('agent_feedback')
    # status=1表示未处理的信息
    modify_info = list(agent_feedback.find({'status': 1}))
    #商务先提交的排在前面
    modify_info.sort(key=lambda x: x['timestamp'])
    # 处理数据
    for info in modify_info:
        info['timestamp'] = info['timestamp'].strftime("%Y-%m-%d")
        # 将honor转为字符串，便于前台js处理
        if info['honor'] != [] and info['honor'] != None:
            honors_str = ''
            for honor in info['honor']:
                if honors_str != '':
                    honors_str += (' ' + honor)
                else:
                    honors_str += honor
            info['honor'] = honors_str
        else:
            info['honor'] = ''
        # 将domain转为字符串，便于前台js处理
        if info['domain'] != [] and info['domain'] != None:
            domain_str = ''
            for domain in info['domain']:
                if domain_str != '':
                    domain_str += (' ' + domain)
                else:
                    domain_str += domain
            info['domain'] = domain_str
        else:
            info['domain'] = ''
    return modify_info

def get_info_from_db(teacher_id):
    """
    将处理中的教师的信息从basic_info表中取出，以便于和商务提交的修改信息做对比
    :return: 该教师再basic_info表中的基本信息
    """
    mogo_operator = MongoOperator(**MongoDB_CONFIG)
    collection = mogo_operator.get_collection('basic_info')
    teacher_info_from_db = collection.find_one({"id": teacher_id},
                                               {'_id': 0, 'funds_id': 0, 'patent_id': 0, 'paper_id': 0})
    if teacher_info_from_db['honor'] != [] and teacher_info_from_db['honor'] != None:
        honors_str = ''
        for honor in teacher_info_from_db['honor']:
            if honors_str != '':
                honors_str += (' ' + honor)
            else:
                honors_str += honor
        teacher_info_from_db['honor'] = honors_str
    if 'domain' in teacher_info_from_db:
        if teacher_info_from_db['domain'] != [] and teacher_info_from_db['domain'] != None:
            domain_str = ''
            for domain in teacher_info_from_db['domain']:
                if domain_str != '':
                    domain_str += (' ' + domain)
                else:
                    domain_str += domain
            teacher_info_from_db['domain'] = domain_str
    else:
        teacher_info_from_db['domain'] = ''
    if 'department' not in teacher_info_from_db:
        teacher_info_from_db['department'] = ''
    return teacher_info_from_db

def get_max_teacher_id():
    """
    获取basci_info中的id最大值，即mysql中的teacher_id的最大值
    :return 当前最大的id值
    """
    mogo_operator = MongoOperator(**MongoDB_CONFIG)
    collection = mogo_operator.get_collection('basic_info')
    max_id_cursor= collection.find({}).sort([('id', -1)]).limit(1)
    max_id =list(max_id_cursor)[0].get('id')
    return max_id

def update_status(obj_id):
    """
    根据_id将agent_feed中的那条数据status设置为0
    """
    mogo_operator = MongoOperator(**MongoDB_CONFIG)
    agent_feedback_collection = mogo_operator.get_collection('agent_feedback')
    try:
        agent_feedback_collection.update_one({'_id': obj_id}, {'$set': {'status': 0}})
    except  Exception as e:
        print(e.args)

def insert_basic_info(data,obj_id):
    """
    将一条记录插入basic_info表中,并根据_id将agent_feed中的那条数据status设置为0
    """
    mogo_operator = MongoOperator(**MongoDB_CONFIG)
    collection = mogo_operator.get_collection('basic_info')
    agent_feedback_collection= mogo_operator.get_collection('agent_feedback')
    try:
        collection.insert_one(data)
        # 将商务反馈的记录标注为已处理
        agent_feedback_collection.update_one({'_id': obj_id}, {'$set': {'status': 0}})
    except Exception as e:
        print(e.args)

def update_basic_info(teacher_id,obj_id,data):
    """
    修改basic_info中的一条记录，并根据_id将agent_feed中的那条数据status设置为0
    :return:
    """
    mogo_operator = MongoOperator(**MongoDB_CONFIG)
    collection = mogo_operator.get_collection('basic_info')
    try:
        agent_feedback_collection= mogo_operator.get_collection('agent_feedback')
        collection.update_one({'id': int(teacher_id)}, {'$set': {'name': data.get('name'),
                                                                      'school': data.get('school'),
                                                                      'institution': data.get('institution'),
                                                                        'department':data.get('department'),
                                                                      'birth_year': data.get('birth_year'),
                                                                      'title': data.get('title'),
                                                                      'honor': data.get('honor'),
                                                                      'domain': data.get('domian'),
                                                                      'email': data.get('email'),
                                                                      'office_number': data.get('office_number'),
                                                                      'phone_number': data.get('phone_number'),
                                                                      'edu_exp': data.get('edu_exp')}})
        # 将商务反馈的记录标注为已处理
        agent_feedback_collection.update_one({'_id': obj_id}, {'$set': {'status': 0}})
    except Exception as e:
        print(e.args)

def get_school():
    """
    获取数据库中所有学校名
    :return:
    """

    mongo_operator = MongoOperator(**MongoDB_CONFIG)
    school = mongo_operator.get_collection("basic_info")
    school_list = school.distinct("school")
    return school_list

def get_institution(school_name):
    """
    根据学校名获取这个学校的所有学院名
    :param school_name: 学校名
    :return: institution:学院名
    """
    mongo_operator = MongoOperator(**MongoDB_CONFIG)
    school = mongo_operator.get_collection("basic_info")
    institution = school.distinct("institution",{"school":school_name})
    return institution

def get_teacher_info(school,institution,teacher):
    """
    根据学校名，学院名和教师名获取教师信息
    :param school:学校名
    :param institution: 学院名
    :param teacher: 教师名
    :return: teacher_dict:教师名、学校名、学院名、头衔、出生年月、邮箱、办公电话、手机号码、教育经历
    """
    mongo_operator = MongoOperator(**MongoDB_CONFIG)
    teacher_list = mongo_operator.get_collection("basic_info")
    if institution == "":
        teacher_dict = teacher_list.find_one({"school":school,"institution":institution,"name":teacher})
    else:
        teacher_dict = teacher_list.find_one({"school":school,"name":teacher})
    return teacher_dict

if __name__ == "__main__":
    #测试
    r = get_teacher_info("东南大学","软件学院","周德宇")
    print(r)