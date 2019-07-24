"""
用户管理的增加、删除、修改、查询
by:董峰
"""

from flask import Blueprint, render_template, request, json
from datetime import datetime
from web_admin.service import user_manage_service
from web_admin.blueprints.auth import login_required
admin_user_bp = Blueprint('admin_user', __name__)
auth_bp = Blueprint('auth', __name__)


@admin_user_bp.route('/user_info')
@login_required
def user_info():
    user = user_manage_service.get_user()
    return render_template('user_info.html',user=user)


@admin_user_bp.route('/add_user', methods=["POST"])
@login_required
def add_user():
    """
    增加用户
    :return:
    """
    date = datetime.utcnow()
    userlist = user_manage_service.get_user()
    # 获取最大id
    userlist.sort(key=lambda ele: ele[4], reverse=True)
    # 接受数据
    name = request.form.get("name")
    tel_number = request.form.get('tel_number')
    email = request.form.get("email")
    school = request.form.get("school")
    school_list = school.split(" ")
    user_type = request.form.get("type")
    if user_type == "高校商务":
        user_type = "0"
    else:
        user_type = "1"
    user = {
        "tel_number": tel_number,
        "type": user_type,
        "creation_time": date,
        "status": "1",
        "id": userlist[0][4]+1,
        "password": "3b86247f12fa88a116e8e446614b3eae",
        "name": name,
        "email": email,
        "charge_school": school_list
    }
    try:
        user_manage_service.add_user(user)
        return json.dumps({"success": True, "message": "添加成功"})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "message": "添加失败"})


@admin_user_bp.route("/del_user", methods=['POST'])
@login_required
def del_user():
    """
    根据用户id删除数据
    :return:
    """
    id = request.form.get("id")
    try:
        back = user_manage_service.delete_user(int(id))
        if back.modified_count > 0:
            return json.dumps({"success": True, "message": "删除成功"})

        return json.dumps({"success": False, "message": "删除失败"})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "message": "出现错误"})


@admin_user_bp.route("/update_user", methods=['POST'])
@login_required
def update_user():
    """
    更新用户信息，包括用户名、联系电话、邮箱、所在学校和用户类型
    :return:
    """
    id = int(request.form.get("id"))
    name = request.form.get("name")
    tel_number = request.form.get("tel_number")
    email = request.form.get("email")
    school = request.form.get("school")
    school = school.split(",")
    user_type = request.form.get("type")

    if user_type == "高校商务":
        user_type = "0"
    else:
        user_type = "1"

    user_dict = {
        "id": id,
        "tel_number": tel_number,
        "type": user_type,
        "name": name,
        "email": email,
        "charge_school": school
    }
    try:
        user_manage_service.update_user(user_dict)
        return json.dumps({"success": True, "massage": "更新成功"})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "message": "更新失败，请稍后重试"})
