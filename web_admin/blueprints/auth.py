from flask import Blueprint, session, redirect, url_for, render_template, flash, request
from web_admin.forms import LoginForm
import functools
from web_admin.service import user_service
from web_admin.utils.mongo_operator import MongoOperator
from web_admin.config import MongoDB_CONFIG
from web_admin.service.teacher_info_service import data_pretreate
from bson.objectid import ObjectId


auth_bp = Blueprint('auth', __name__)


def login_required(func):
    """
    装饰函数，如果需要某函数需要登陆后操作，则可以装饰上此函数
    如@login_required
    """
    @functools.wraps(func)
    def wrapper(*args, **kw):
        # 当前未登陆
        user = session.get('username')
        if user is None:
            return redirect(url_for('auth.login'))
        return func(*args, **kw)
    return wrapper


@auth_bp.route('/')
def index():
    if 'username' in session:
        mogo_operator = MongoOperator(**MongoDB_CONFIG)
        # 从数据库中取出商务提交的所有信息
        agent_feedback = mogo_operator.get_collection('agent_feedback')
        # status=0表示未处理的信息
        modify_info = list(agent_feedback.find({'status': 1}))
        modify_info.sort(key=lambda x: x['timestamp'])
        # 处理数据
        for info in modify_info:
            info['timestamp'] = info['timestamp'].strftime("%Y-%m-%d")
            # 将honor转为字符串，便于前台js处理
            if 'honor_title' in info:
                honor_title_list = []
                if info['honor_title'] != []:
                    for title in info['honor_title']:
                        honor_title_list.append({'type': title, 'year': ''})
                info['honor_title'] = honor_title_list
            data_pretreate(info)
        return render_template('teacher_info.html',modify_info =modify_info)
    else:
        return  render_template("login.html")


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

    user = user_service.check_user(username, password)
    # 检验账号密码
    if user:
        session['username'] = user["name"]
        session['uid'] = user["id"]
        mogo_operator = MongoOperator(**MongoDB_CONFIG)
        # 从数据库中取出商务提交的所有信息
        agent_feedback = mogo_operator.get_collection('agent_feedback')
        # status=0表示未处理的信息
        modify_info = list(agent_feedback.find({'status': 1}))
        modify_info.sort(key=lambda x: x['timestamp'])
        # 处理数据
        for info in modify_info:
            info['timestamp'] = info['timestamp'].strftime("%Y-%m-%d")
            data_pretreate(info)
        return render_template('teacher_info.html',modify_info =modify_info)
    else:
        flash('登录失败，请检测账号或者密码后重新输入', 'danger')
        return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return render_template("login.html")


