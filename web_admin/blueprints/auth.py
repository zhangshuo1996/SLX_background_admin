from flask import Blueprint, session, redirect, url_for, render_template, flash, request
from web_admin.forms import LoginForm
import functools
from web_admin.service import user_service


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
        username = session['username']
        return render_template('base.html',username=username)
    else:
        return  render_template("login.html")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        print(username,password)

    user = user_service.check_user(username, password)
    print(user)
    # 检验账号密码
    if user:
        session['username'] = user["name"]
        session['uid'] = user["id"]
        return render_template('base.html')
    else:
        flash('登录失败，请检测账号或者密码后重新输入', 'danger')
        return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return render_template("login.html")


@auth_bp.route('/products')
@login_required
def products():
    return render_template('products.html')


@auth_bp.route('/accounts')
@login_required
def accounts():
    return render_template('accounts.html')