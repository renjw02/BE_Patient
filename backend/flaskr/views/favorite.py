#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib
from flask import Blueprint, jsonify, request, g
from .login_required import login_required
from flaskr.service import FavoriteService
from flaskr.checkers import favorite_params_check


bp = Blueprint('favorite', __name__, url_prefix='/favorite')

service = FavoriteService()


@bp.route('/api')
def index():
    return 'favorite配置完成!'


@bp.route('/api/createfavor', methods=['POST'])
@login_required
def create_favor():
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "no content"}), 400
        key, passed = favorite_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        fav, result = service.create_favorite(g.user_id, content['post_id'], content['news_id'],
                                        content['title'])

        if result:
            return jsonify({
                'favoriteId': fav.id,
                'userId': fav.user_id,
                'title': fav.title,
                'message': "ok"
            }), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400



@bp.route('/api/getfavorlist', methods=['GET'])
@login_required
def get_favor_list():
    try:
        page = 1 if request.args.get('page') is None else int(request.args.get('page'))
        # type == 0 全部 type == 1 post type == 2 news
        type = 0 if request.args.get('type') is None else int(request.args.get('type'))

        favor_list, count, flag = service.get_fav_list(g.user_id, page, type) 

        if flag:
            return jsonify({
                'message': "ok",
                'favorite_list': favor_list,
                'count': count,
                'page': page,
                'type': type
            }), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


@bp.route('/api/deletefavor', methods=['GET'])
@login_required
def delete_favor():
    try:
        id = request.args.get('favorite_id')

        check = service.check_favor(g.user_id, id)
        if not check:
            return jsonify({'message': "not found"}), 404
            
        result = service.delete_favorite(id)

        if result:
            return jsonify({'message': "ok",}), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


@bp.route('/api/checkfavor', methods=['GET'])
@login_required
def check_favor():
    try:
        post_id = int(request.args.get('post_id'))
        news_id = int(request.args.get('news_id'))

        if post_id == 0 and news_id == 0:
            return jsonify({'message': "need to be a post or a news"}), 500

        if post_id == 0:
            favor, result = service.check_favorite_news(g.user_id, news_id)
        elif news_id == 0:
            favor, result = service.check_favorite_post(g.user_id, post_id)
            
        if result:
            return jsonify({
                'message': "ok",
                'favorite_id': favor.id}), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400