#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib
import os

from flask import Blueprint, jsonify, request, g, make_response
from flaskr.service import UserService
from flaskr.checkers import register_params_check, change_params_check
from flaskr.utils import generate_jwt
from .login_required import login_required

bp = Blueprint('user', __name__, url_prefix='/user')

service = UserService()

@bp.route('/api')
def index():
    return jsonify({'message': "user配置完成!"}), 200

@bp.route('/api/register', methods=['POST'])
def user_register():
    """
    注册
    """
    try:
        content = request.get_json()
        if not content:
            return jsonify({'message': "no content"}), 400
        key, passed = register_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        user, flag = service.create_user(content['username'],
                                   content['password'],
                                   content['nickname'],
                                   content['mobile'],
                                   content['address'],
                                   content['signature'])

        if flag:
            return jsonify({
                'message': "ok",
                'userId' : user.id,
                'username': user.username,
                'nickname': user.nickname
            }), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


@bp.route('/api/login', methods=['POST'])
def login():
    """
    登陆
    """
    try:
        content = request.get_json()
        if not content:
            return jsonify({'message': "bad arguments"}), 400

        user, flag = service.get_user_by_name_and_pass(content['username'], content['password'])
        if user.status == 1:
            return jsonify({'message': "user has already logged in"}), 300

        if flag:
            service.login(user.id)
            jwt = generate_jwt({
                "user_id": user.id,
                "nickname": user.nickname
            })

            return jsonify({
                "jwt": jwt,
                "userId": user.id,
                "username": user.username,
                "nickname": user.nickname,
            }), 200
        else:
            return jsonify({'message': user}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


@bp.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """
    登出
    """
    try:
        flag = service.logout(g.user_id)
        if flag:
            return jsonify({'message': "ok"}), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


# id传整数
@bp.route('/api/changeattr', methods=['POST'])
@login_required
def change_attr():
    """
    改变属性
    """
    try:
        content = request.get_json()
        if not content:
            return jsonify({'message': "no content"}), 400
        # print(content)

        key, passed = change_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400
        
        user, flag = service.change_attr(g.user_id, content['username'],
                                content['nickname'], content['mobile'], content['address'],
                                content['signature'])

        if flag:
            return jsonify({
                'message': "ok",
                'username': user.username,
                'nickname': user.nickname,
                'mobile': user.mobile,
                'address': user.address,
                'signature': user.signature
                }), 200
        else:
            return jsonify({'message': user}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400    


@bp.route('/api/user', methods=['GET'])
@login_required
def get_user_info():
    """
    获取当前登录用户信息
    """
    user, flag = service.get_user(g.user_id)
    if flag:
        return jsonify({
            "id":       user.id,
            "username": user.username,
            "nickname": user.nickname,
            "created":  user.created,
            "mobile": user.mobile,
            "address": user.address,
            "signature": user.signature
        }), 200
    else:
        return jsonify({'message': user}), 500


@bp.route('/api/user/<int:userId>', methods=['GET'])
@login_required
def get_user_info_by_id(userId):
    """
    获取指定用户信息
    """
    user, flag = service.get_user(userId)
    if flag:
        return jsonify({
            "id":       user.id,
            "nickname": user.nickname,
            "created":  user.created,
            "signature": user.signature,
        }), 200
    else:
        return jsonify({'message': user}), 500



@bp.route('/api/resetpw', methods=['POST'])
def reset_password():
    """
    忘记密码
    """
    try:
        content = request.get_json()
        if not content:
            return jsonify({'message': "no content"}), 400

        if 'username' in content and 'mobile' in content:
            pass
        else:
            return jsonify({'message': "lack parameters"}), 400
        
        user, flag = service.reset_pw(content['username'], content['mobile'], content['password'])
        if flag:
            return jsonify({
                'message': "ok",
                'user_id': user.id,
                'username': user.username,
                'nickname': user.nickname,
                'mobile': user.mobile,
                'address': user.address,
                'signature': user.signature
                }), 200
        else:
            return jsonify({'message': user}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400    


# 上传头像
@bp.route('/api/uploadavatar', methods=['POST'])
@login_required
def upload_avatar():
    try:
        file_obj = request.files.get('file')
        file_name = file_obj.filename
        save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "static", "avatar", str(file_name)))
        file_obj.save(save_path)
        workpath = os.getcwd()
        dst = os.path.join(workpath, 'flaskr', 'static', 'avatar', str(g.user_id)+'.jpg')
        if os.path.exists(dst):
            os.remove(dst)
        os.rename(save_path, dst)
        return jsonify({'message': "ok"}), 200
    except:
        return jsonify({'message': "error"}), 400  


# 获取头像
@bp.route('/api/downloadavatar', methods=['GET'])
@login_required
def download_avatar():
    try:
        file_name = request.args['name']
        if file_name is None:
             return jsonify({'message': "no file name"}), 400
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "static", "avatar", str(file_name)))
        # print(path)
        imageData = open(path, "rb").read()
        response = make_response(imageData)
        response.headers['Content-Type'] = 'image/jpeg'
        return response, 200
    except:
        return jsonify({'message': "error"}), 400  

