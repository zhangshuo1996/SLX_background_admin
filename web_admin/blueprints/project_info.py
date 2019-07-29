"""
by dxy
2019/7/23
"""
from flask import Blueprint, render_template, session, request
import json
from web_admin.blueprints.auth import login_required
from bson.objectid import ObjectId
from web_admin.service import project_info_service
import datetime

project_info_bp = Blueprint('project_info', __name__)

@project_info_bp.route('/project_info')
@login_required
def project_info():
    """
    从数据库中将未处理的项目信息取出，发送给前端展示
    """
    project_info = project_info_service.get_project_info()
    return render_template('project_info.html',project_info = project_info)

@project_info_bp.route('/project_data_preservation',methods = ['POST'])
@login_required
def project_data_preservation():
    """
    将审核过后的项目信息保存到数据库，并将这条信息的状态设置为已处理
    """
    _id = request.form.get('_id')
    #将members转换为list,第一个人为负责人
    members_str = request.form.get('members')
    members = eval(members_str)
    #将起始时间转为datatime格式
    # start_time = datetime.datetime.strptime(request.form.get('start_time'), '%Y-%m-%d')
    # end_time = datetime.datetime.strptime(request.form.get('end_time'), '%Y-%m-%d')
    #将 万元去掉，并转换为浮点型
    fund = float(request.form.get('fund').split()[0])
    data = {
        'name':request.form.get('name'),
        'project_type':request.form.get('project_type'),
        'fund':fund,
        'start_time':request.form.get('start_time'),
        'end_time':request.form.get('end_time'),
        'members':members,
        'company':request.form.get('company'),
        'content':request.form.get('content')
    }
    try:
        project_info_service.insert_project_info(data,_id)
        return json.dumps({"success": True, "message": "操作成功"})
    except Exception as e:
        print(e.args)
        return json.dumps({"success": False, "message": "操作失败"})

@project_info_bp.route('/project_data_ignore', methods=['POST'])
@login_required
def data_ignore():
    """
    忽略商务提交的消息
    """
    _id = ObjectId(request.form.get('_id'))
    try:
        project_info_service.update_status(_id)
        return json.dumps({"success": True, "message": "操作成功"})
    except Exception as e:
        print(e.args)
        return json.dumps({"success": False, "message": "操作失败"})
