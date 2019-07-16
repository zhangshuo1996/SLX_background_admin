from flask import Blueprint, render_template, session, request
import functools

from web_admin.blueprints.auth import login_required
from web_admin.utils.mongo_operator import MongoOperator
from web_admin.config import MongoDB_CONFIG
#from web_admin.settings import basedir

#蓝图要注册，在utils/__init__.py中，from web_admin.blueprints.teacher_info import teacher_info_bp，在register_blueprints函数中注册
#TODO
teacher_info_bp = Blueprint('teacher_info', __name__)
@teacher_info_bp.route('/teacher_info')
@login_required
def teacher_info():
    return render_template('products.html')


