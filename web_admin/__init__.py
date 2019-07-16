import os
from flask import Flask, render_template, session
from web_admin.settings import configuration
from web_admin.extensions import bootstrap,moment
from web_admin.utils.mongo_operator import MongoOperator
from web_admin.config import MongoDB_CONFIG
from web_admin.blueprints.auth import auth_bp
from web_admin.blueprints.teacher_info import teacher_info_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', "development")

    app = Flask('web_admin')
    app.config.from_object(configuration[config_name])

    # 注册日志处理器
    register_logging(app)
    # 初始化扩展
    register_extensions(app)
    # 注册蓝图
    register_blueprints(app)
    # 注册错误处理函数
    register_errors(app)
    # 注册模板上下文处理函数
    # register_template_context(app)

    return app


def register_logging(app):
    pass


def register_extensions(app):
    bootstrap.init_app(app)
    # csrf.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html', description="会话过期或失效，请返回上一页重试"), 400


# def register_template_context(app):
#     """注册模板上下文，使得变量可以在模板中使用"""
#     @app.context_processor
#     def make_template_context():
#         # 如果登录，则尝试拉取未读信息
#         unread_msg = 0
#         if 'username' in session:
#             uid = session['uid']
#             mongo_operator = MongoOperator(**MongoDB_CONFIG)
#             unread_msg = mongo_operator.find({"to_id": uid, "state": 0}, "message").count()
#
#         return dict(unread_msg=unread_msg)


