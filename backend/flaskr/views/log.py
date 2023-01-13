#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib
from flask import Blueprint, jsonify, request, g
from .login_required import login_required
from flaskr.service import LogService
from flaskr.checkers import log_params_check


bp = Blueprint('log', __name__, url_prefix='/log')

service = LogService()


@bp.route('/api')
def index():
    return 'log配置完成!'


@bp.route('/api/createlog', methods=['POST'])
@login_required
def create_log():
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "no content"}), 400
        key, passed = log_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        if 'log_date' in content:
            log_date = content['log_date']
        else:
            log_date = 0
        log, result = service.create_log(g.user_id, content['title'], content['content'], log_date)

        if result:
            return jsonify({
                'logId': log.id,
                'userId': log.user_id,
                'title': log.title,
                'content': log.content,
                'date': log.date,
                'message': "ok"
            }), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


# 获取log
@bp.route('/api/getlog', methods=['GET'])
@login_required
def get_log():
    try:
        date = request.args.get("date")
        if date is None:
            return jsonify({'message': "no date"}), 400

        myLog, flag = service.get_log(g.user_id, date) 

        if flag:
            return jsonify({
                'message': "ok",
                'log_id': myLog.id,
                'title': myLog.title,
                'content': myLog.content,
                'date': myLog.date,
                'created': myLog.created,
                'updated': myLog.updated
            }), 200
        else:
                return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


@bp.route('/api/updatelog', methods=['POST'])
@login_required
def update_log():
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "no content"}), 400
        key, passed = log_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        check = service.check_log(g.user_id, content['log_id'])
        if not check:
            return jsonify({'message': "not found"}), 404
            
        result = service.update_log(content['log_id'], content['title'], content['content'])

        if result:
            return jsonify({'message': "ok",}), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400