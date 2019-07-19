from flask import Blueprint, render_template, session, request
import time,datetime
import json

from web_admin.blueprints.auth import login_required
from web_admin.utils.mongo_operator import MongoOperator
from web_admin.config import MongoDB_CONFIG
from bson.objectid import ObjectId
#from web_admin.settings import basedir

#蓝图要注册，在utils/__init__.py中，from web_admin.blueprints.teacher_info import teacher_info_bp，在register_blueprints函数中注册
#TODO 1.将数据库中商务提交的信息从数据库中拉取出来，列在teacher_info.html上2.点击商务的某条信息，将在左边弹出信息3.点击保存，将信息保存到数据库，并将商务提交的数据在数据库中标注为已处理，点击
#TODO 忽略，商务提交的数据标注为已处理 4.页面：提交的数据和数据库数据做对比，不一样的标出来5.新增教师信息处理6.页面字体横竖，布局修改
teacher_info_bp = Blueprint('teacher_info', __name__)

@teacher_info_bp.route('/teacher_info')
@login_required
def teacher_info():
    mogo_operator = MongoOperator(**MongoDB_CONFIG)
    #从数据库中取出商务提交的所有信息
    agent_feedback= mogo_operator.get_collection('agent_feedback')
    #status=0表示未处理的信息
    modify_info = list(agent_feedback.find({'status':1}))
    modify_info.sort(key=lambda x: x['timestamp'])
    #处理数据
    for info in modify_info:
        info['timestamp'] = info['timestamp'].strftime("%Y-%m-%d")
        # 将honor转为字符串，便于前台js处理
        if info['honor'] != [] and info['honor'] != None:
            honors_str= ''
            for honor in info['honor']:
                if honors_str != '':
                    honors_str += (' '+honor)
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
                    domain_str += (' '+domain)
                else:
                    domain_str += domain
            info['domain'] = domain_str
        else:
            info['domain'] =''
    return render_template('teacher_info.html',modify_info =modify_info)

@teacher_info_bp.route('/get_info_by_tid',methods=['POST'])
@login_required
def get_info_by_tid():
    teacher_id = request.form.get('teacher_id', type=int)
    #根据id从数据中获取教师信息
    mogo_operator = MongoOperator(**MongoDB_CONFIG)
    collection =mogo_operator.get_collection('basic_info')
    teacher_info_from_db = collection.find_one({"id":teacher_id}, {'_id': 0, 'funds_id': 0, 'patent_id': 0, 'paper_id': 0})
    if teacher_info_from_db['honor'] != [] and teacher_info_from_db['honor'] != None:
        honors_str= ''
        for honor in teacher_info_from_db['honor']:
            if honors_str != '':
                honors_str += (' '+honor)
            else:
                honors_str += honor
        teacher_info_from_db['honor'] = honors_str
    print(teacher_info_from_db)
    if 'domain' in teacher_info_from_db:
        if teacher_info_from_db['domain'] != [] and teacher_info_from_db['domain'] != None:
            domain_str= ''
            for domain in teacher_info_from_db['domain']:
                if domain_str != '':
                    domain_str += (' '+domain)
                else:
                    domain_str += domain
            teacher_info_from_db['domain'] = domain_str
    else:
        teacher_info_from_db['domain'] = ''
    if 'department' not in teacher_info_from_db:
        teacher_info_from_db['department'] = ''
    print(teacher_info_from_db)
    return json.dumps(teacher_info_from_db,ensure_ascii=False)

@teacher_info_bp.route('/data_preservation', methods=['POST'])
@login_required
def data_preservation():
    """
    将商务提交的数据保存到数据库
    :return:
    """
    mogo_operator = MongoOperator(**MongoDB_CONFIG)
    collection = mogo_operator.get_collection('basic_info')
    agent_feedback_collection= mogo_operator.get_collection('agent_feedback')
    teacher_id = request.form.get('teacher_id')
    honor_str= request.form.get('honor')
    if honor_str != '' and honor_str != None:
        honors = honor_str.split(' ')
    else:
        honors = []
    print(honors)
    domain_str = request.form.get('domain')
    if domain_str != ''and domain_str != None:
        domain = domain_str.split(' ')
    else:
        #防止domain出现['']的情况
        domain = []
    print(domain)
    data = {
        'name':request.form.get('name'),
        'school':request.form.get('school'),
        'institution':request.form.get('institution'),
        'department':request.form.get('department'),
        'birth_year':request.form.get('birth_year'),
        'title':request.form.get('title'),
        'honor':honors,
        'domain':domain,
        'email':request.form.get('email'),
        'office_number':request.form.get('office_number'),
        'phone_number':request.form.get('phone_number'),
        'edu_exp':request.form.get('edu_exp'),
        'id':teacher_id,
        'position':'',
        'patrnt_id':[],
        'funds_id':[],
        'paper_id':[]
    }
    obj_id = ObjectId(request.form.get('object_id'))
    if teacher_id == "None" or teacher_id == None or teacher_id == '':
    #处理新增数据
        max_id = get_max_teacher_id()
        data['id'] = max_id+1
        try:
            collection.insert_one(data)
            # 将商务反馈的记录标注为已处理
            agent_feedback_collection.update_one({'_id':obj_id},{'$set':{'status':0}})

            return json.dumps({"success": True, "message": "操作成功"})
        except:
            return json.dumps({"success": False, "message": "操作失败"})
    else:
    #处理修改数据
        try:
            result = collection.update_one({'id':int(teacher_id)},{'$set':{'name':request.form.get('name'),
                                                            'school':request.form.get('school'),
                                                            'institution':request.form.get('institution'),
                                                            'birth_year':request.form.get('birth_year'),
                                                            'title':request.form.get('title'),
                                                            'honor':honors,
                                                           'domain':domain,
                                                            'email':request.form.get('email'),
                                                            'office_number':request.form.get('office_number'),
                                                            'phone_number':request.form.get('phone_number'),
                                                            'edu_exp':request.form.get('edu_exp')}})

        # 将商务反馈的记录标注为已处理


            agent_feedback_collection.update_one({'_id': obj_id}, {'$set': {'status': 0}})
            return json.dumps({"success": True, "message": "操作成功"})
        except:
            return json.dumps({"success": False, "message": "操作失败"})



@teacher_info_bp.route('/data_ignore', methods=['POST'])
@login_required
def data_ignore():
    """
    忽略商务提交的消息
    """
    obj_id = ObjectId(request.form.get('object_id'))
    mogo_operator = MongoOperator(**MongoDB_CONFIG)
    agent_feedback_collection = mogo_operator.get_collection('agent_feedback')
    agent_feedback_collection.update_one({'_id': obj_id}, {'$set': {'status': 0}})
    return json.dumps({"success": True, "message": "操作成功"})



def get_max_teacher_id():
    """
    获取basci_info中的id最大值，即mysql中的teacher_id的最大值
    """
    mogo_operator = MongoOperator(**MongoDB_CONFIG)
    collection = mogo_operator.get_collection('basic_info')
    max_id_cursor= collection.find({}).sort([('id', -1)]).limit(1)
    max_id =list(max_id_cursor)[0].get('id')
    return max_id