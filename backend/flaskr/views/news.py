#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib

from flask import Blueprint, jsonify, request, g
from flaskr.service import NewsService

bp = Blueprint('news', __name__, url_prefix='/news')

service = NewsService()

@bp.route('/api')
def index():
    return 'news配置完成!'

# 获取资讯内容
@bp.route('/api/news/<int:newsId>', methods=['GET'])
def get_news_detail(newsId):
    news, result = service.get_news(newsId)
    if result:
        import os
        file_path = news.address
        file = open(file_path, 'r', encoding='utf-8')
        content = file.read()
        file.close()
        return jsonify({
            'content': content,
            'id': news.id,
            'title': news.title,
            'date': news.date
        }), 200
    else:
        return jsonify({'message': "error"}), 500


# 获取一页的资讯列表
@bp.route('/api/getnewslist', methods=['GET'])
def get_news_list():
    page = 1 if request.args.get('page') is None else int(request.args.get('page'))
    keyword = 0 if request.args.get('keyword') is None else int(request.args.get('keyword'))

    news_list, count, result = service.get_news_list(page, 10, keyword)

    # count 帖子总数
    if result:
        return jsonify({
            'news': news_list,
            'page': page,
            'total': count,
            'message': "ok"
        }), 200
    else:
        return jsonify({'message': "error"}), 500


# 获取一页的资讯列表
@bp.route('/api/getnewsbysearch', methods=['GET'])
def get_news_list_by_search():
    page = 1 if request.args.get('page') is None else int(request.args.get('page'))
    word = request.args.get('search_word')
    if word is None:
        return jsonify({'message': "no search word"}), 400

    news_list, count, result = service.get_news_list_by_search(word, page)

    # count 帖子总数
    if result:
        return jsonify({
            'news': news_list,
            'page': page,
            'total': count,
            'message': "ok"
        }), 200
    else:
        return jsonify({'message': "error"}), 500