from flask import Blueprint, render_template, session, request
import functools

from web_admin.blueprints.auth import login_required
from web_admin.utils.mongo_operator import MongoOperator
from web_admin.config import MongoDB_CONFIG
#from web_admin.settings import basedir

#蓝图要注册，在utils/__init__.py中，from web_admin.blueprints.teacher_info import teacher_info_bp，在register_blueprints函数中注册
#TODO 1.将数据库中商务提交的信息从数据库中拉取出来，列在teacher_info.html上2.点击商务的某条信息，将在左边弹出信息3.点击保存，将信息保存到数据库，并将商务提交的数据在数据库中标注为已处理，点击
#TODO 忽略，商务提交的数据标注为已处理 4.页面：提交的数据和数据库数据做对比，不一样的标出来5.新增教师信息处理
teacher_info_bp = Blueprint('teacher_info', __name__)

@teacher_info_bp.route('/teacher_info')
@login_required
def teacher_info():
    mogo_operator = MongoOperator(**MongoDB_CONFIG)
    modify_info = mogo_operator.find()
    return render_template('teacher_info.html')

# @teacher_info_bp.route('/teacher_info/info_display')
# @login_required
# def info_display():



