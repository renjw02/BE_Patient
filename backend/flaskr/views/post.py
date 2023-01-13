#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib
from flask import Blueprint, jsonify, request, g
from .login_required import login_required
from flaskr.service import PostService
from flaskr.checkers import post_params_check, reply_params_check

bp = Blueprint('post', __name__, url_prefix='/post')

service = PostService()

@bp.route('/api')
def index():
    return 'post配置完成!'

# 创建帖子
@bp.route('/api/createpost', methods=['POST'])
@login_required
def create_post():
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "no content"}), 400
        key, passed = post_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        post, result = service.create_post(content['title'], content['content'], g.user_id)

        if result:
            return jsonify({
                'postId': post.id,
                'userId': post.user_id,
                'title': post.title,
                'content': post.content,
                'message': "ok"
            }), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400

# 获取指定帖子信息
@bp.route('/api/getpost/<int:postId>', methods=['GET'])
@login_required
def get_post_detail(postId):
    detail, result = service.get_post_detail(postId)
    if result:
        return jsonify(detail), 200
    else:
        return jsonify({'message': "error"}), 500

# 获取一页的帖子列表
@bp.route('/api/getpostlist', methods=['GET'])
@login_required
def get_post_list():
    page = 1 if request.args.get('page') is None else int(request.args.get('page'))
    size = 10 if request.args.get('size') is None else int(request.args.get('size'))
    user_id = 0 if request.args.get('userId') is None else request.args.get('userId')
    order_by_reply = False if request.args.get('orderByReply') is None else True

    post_list, count, result = service.get_post_list(user_id, page, size, order_by_reply)

    # count 帖子总数
    if result:
        return jsonify({
            'posts': post_list,
            'page': page,
            'size': size,
            'total': count
        }), 200
    else:
        return jsonify({'message': "error"}), 500

# 修改指定帖子
@bp.route('/api/modifypost/<int:postId>', methods=['POST'])
@login_required
def modify_post(postId):
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "no content"}), 400
        key, passed = post_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        check = service.check_post(postId, g.user_id)
        if not check:
            return jsonify({'message': "not found"}), 404

        result = service.update_post(content['title'], content['content'], postId, g.user_id)

        if result:
            return jsonify({'message': "ok"}), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


# 删除指定帖子
@bp.route('/api/deletepost/<int:postId>', methods=['POST'])
@login_required
def delete_post(postId):
    try:
        check = service.check_post(postId, g.user_id)
        if not check:
            return jsonify({'message': "not found"}), 404

        post, flag = service.get_post_detail(postId)
        if not flag: 
            return jsonify({'message': "not found"}), 404
        
        id_list = []
        for reply in post['reply']:
            id_list.append(reply['id'])

        for id in id_list:
            flag = service.delete_reply(id)
            if not flag:
                return jsonify({'message': "delete error"}), 400
            # id_list = list(map(lambda x:x-1, id_list))

        result = service.delete_post(postId)

        if result:
            return jsonify({'message': "ok"}), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


# 回复帖子
@bp.route('/api/reply/<int:postId>', methods=['POST'])
@login_required
def reply_post(postId):
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "no content"}), 400

        key, passed = reply_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400
        if "replyId" in content:
            reply_id = content['replyId']
        else:
            reply_id = 0

        # 检查回复是否是对应帖子的回复
        check = service.check_reply(postId, reply_id)
        if not check:
            return jsonify({'message': "not found"}), 404

        result = service.create_reply(content['content'], g.user_id, postId, reply_id)

        if result:
            return jsonify({'message': "ok"}), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


# 删除指定回复
@bp.route('/api/deletereply/<int:replyId>', methods=['POST'])
@login_required
def delete_reply(replyId):
    try:
        check = service.check_self_reply(replyId, g.user_id)
        if not check:
            return jsonify({'message': "not found"}), 404
        
        reply_list, flag = service.get_reply_list(replyId)
        if not flag: 
            return jsonify({'message': "not found"}), 404

        id_list = []
        for reply in reply_list:
            id_list.append(reply['id'])
        
        for id in id_list:
            flag = service.delete_reply(id)
            if not flag:
                return jsonify({'message': "delete error"}), 400

        result = service.delete_reply(replyId)

        if result:
            return jsonify({'message': "ok"}), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


# 获取回复
@bp.route('/api/getreply', methods=['GET'])
@login_required
def get_reply():
    try:
        reply_id = request.args['reply_id']
        if reply_id == 0:
            return jsonify({'message': "not a reply"}), 400
        reply, flag = service.get_reply(reply_id)

        if flag:
            return jsonify({
                'message': "ok",
                "user_id": reply.user_id,
                "reply_id": reply.reply_id,
                "post_id": reply.post_id,
                "content": reply.content,
                "favor_num": reply.favor_num,
            }), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


# 获取回复列表
@bp.route('/api/getreplylist', methods=['GET'])
@login_required
def get_reply_list():
    try:
        reply_id = request.args['reply_id']
        if reply_id == 0:
            return jsonify({'message': "not a reply"}), 400
        reply_list, flag = service.get_reply_list(reply_id)

        if flag:
            return jsonify({
                'message': "ok",
                'reply_list': reply_list
            }), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


# 修改回复
@bp.route('/api/modify/<int:postId>/reply/<int:replyId>', methods=['POST'])
@login_required
def modify_reply(postId, replyId):
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "no content"}), 400

        key, passed = reply_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        # 检验回复是否是当前用户的回复
        check = service.check_self_reply(replyId, g.user_id)
        if not check:
            return jsonify({'message': "not found"}), 404

        result = service.update_reply(
            content['content'], g.user_id, postId, replyId)

        if result:
            return jsonify({'message': "ok"}), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


# 点赞帖子
@bp.route('/api/supportpost/<int:postId>', methods=['POST'])
@login_required
def support_post(postId):
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "no content"}), 400

        if 'type' in content:
            if content['type'] != 1 and content['type'] != -1:
                return jsonify({'message': "error type input"}), 400
        else:
            return jsonify({'message': "no type"}), 400

        msg, result = service.support_post(postId, content['type'])

        if result:
            return jsonify({'message': msg}), 200
        else:
            return jsonify({'message': msg}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


# 点赞回复
@bp.route('/api/supportreply/<int:replyId>', methods=['POST'])
@login_required
def support_reply(replyId):
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "no content"}), 400

        if 'type' in content:
            if content['type'] != 1 and content['type'] != -1:
                return jsonify({'message': "error type input"}), 400
        else:
            return jsonify({'message': "no type"}), 400

        msg, result = service.support_reply(replyId, content['type'])

        if result:
            return jsonify({'message': msg}), 200
        else:
            return jsonify({'message': msg}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400
