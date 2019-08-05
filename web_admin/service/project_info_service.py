"""
by dxy
2019/7/23
"""
from web_admin.utils.mongo_operator import MongoOperator
from web_admin.config import MongoDB_CONFIG
from bson.objectid import ObjectId

def get_project_info() :
    """
    从数据库project_feedback中取得所有未处理的project信息
    :return:
    """
    mogo_operator = MongoOperator(**MongoDB_CONFIG)
    # 从数据库中取出商务提交的所有信息
    project_feedback = mogo_operator.get_collection('project_feedback')
    #status表示未处理的信息
    project_info = list(project_feedback.find({'status': 1}))
    #按商务提交时间排序，先提交的排在前面
    project_info.sort(key=lambda x: x['timestamp'])
    for info in project_info:
        info['timestamp']  = info['timestamp'].strftime("%Y-%m-%d")
        # info['start_time'] = info['start_time'].strftime("%Y-%m-%d")
        # info['end_time'] = info['end_time'].strftime("%Y-%m-%d")
    return project_info

def insert_project_info(data,_id):
    """
    :param data:要保存的项目信息
    :param _id: 已处理的项目信息的_id
    将项目信息保存到数据库，并将project_feedback中的那条信息status置为0
    """
    mogo_operator = MongoOperator(**MongoDB_CONFIG)
    collection = mogo_operator.get_collection('project_info')
    project_feedback_collection= mogo_operator.get_collection('project_feedback')
    try:
        # 将商务反馈的记录标注为已处理
        _id = ObjectId(_id)
        project_feedback_collection.update_one({'_id': _id}, {'$set': {'status': 0}})
        result_insert = collection.insert_one(data)
    except Exception as e:
        print(e.args)

def update_status(_id):
    """
    根据_id将agent_feed中的那条数据status设置为0
    """
    mogo_operator = MongoOperator(**MongoDB_CONFIG)
    project_feedback_collection = mogo_operator.get_collection('project_feedback')
    _id = ObjectId(_id)
    try:
        project_feedback_collection.update_one({'_id': _id}, {'$set': {'status': 0}})
    except  Exception as e:
        print(e.args)


if __name__ == "__main__":
    l = get_project_info()
    print(l)