#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib
from flask import Blueprint, jsonify, request, g
from .login_required import login_required
from flaskr.service import pgService
from flaskr.checkers import pg_params_check

bp = Blueprint('pg', __name__, url_prefix='/pg')

service = pgService()

@bp.route('/api')
def index():
    return 'pg配置完成!'


# 创建pg
@bp.route('/api/createpg', methods=['POST'])
@login_required
def create_pg():
    """
    创建pg
    """
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "no content"}), 400
        
        key, passed = pg_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400
        if 'pg_date' in content:
            pg_date = content['pg_date']
        else:
            pg_date = 0
        pg, result = service.create_pg(g.user_id, pg_date, content['fpg_morning'], content['fpg_noon'],
                                        content['fpg_evening'], content['p2hpg_morning'], 
                                        content['p2hpg_noon'], content['p2hpg_evening'])
        
        if result:
            return jsonify({
                'message': "ok",
                'pg_id': pg.id,
                'fpg_morning': pg.fpg_morning,
                'fpg_noon': pg.fpg_noon,
                'fpg_evening': pg.fpg_evening,
                'p2hpg_morning': pg.p2hpg_morning,
                'p2hpg_noon': pg.p2hpg_noon,
                'p2hpg_evening': pg.p2hpg_evening,
                'pg_date': pg.date
            }), 200
        else:
            return jsonify({'message': "已记录该日"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400

# 获取pg
@bp.route('/api/getpg', methods=['GET'])
@login_required
def get_pg():
    try:
        date = request.args.get("date")
        if date is None:
            return jsonify({'message': "no date"}), 400

        pg, flag = service.get_pg(g.user_id, date) 

        if flag:
            return jsonify({
                'message': "ok",
                'pg': pg
            }), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400

# 更新pg
@bp.route('/api/updatepg', methods=['POST'])
@login_required
def update_pg():
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "no content"}), 400
        key, passed = pg_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400
        
        flag = service.check_pg(content['pg_id'], g.user_id)
        if not flag:
            return jsonify({'message': "not found"}), 400

        result = service.update_pg(content['pg_id'], content['fpg_morning'], content['fpg_noon'],
                                        content['fpg_evening'], content['p2hpg_morning'], 
                                        content['p2hpg_noon'], content['p2hpg_evening'])

        if result:
            return jsonify({'message': "ok",}), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


# 获取pg列表
@bp.route('/api/getpglist', methods=['GET'])
@login_required
def get_pg_list():
    try:
        page = 1 if request.args.get('page') is None else int(request.args.get('page'))

        pg_list, count, flag = service.get_pg_list(g.user_id, page)

        if flag:
            return jsonify({
                'message': 'ok',
                'pg_list': pg_list,
                'count': count
            }), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400


# 获取全部pg
@bp.route('/api/getpgall', methods=['GET'])
@login_required
def get_pg_all():
    try:
        pg_list, count, flag = service.get_pg_all(g.user_id)


        if flag:
            fpg_list = []
            p2hpg_list = []

            for pg in pg_list:
                fpg_list.append({
                    'name': pg['date'],
                    'value': [pg['date']+" 08:00:00", pg['fpg_morning']]
                })
                fpg_list.append({
                    'name': pg['date'],
                    'value': [pg['date']+" 12:00:00", pg['fpg_noon']]
                })
                fpg_list.append({
                    'name': pg['date'],
                    'value': [pg['date']+" 18:00:00", pg['fpg_evening']]
                })
                p2hpg_list.append({
                    'name': pg['date'],
                    'value': [pg['date']+" 10:00:00", pg['p2hpg_morning']]
                })
                p2hpg_list.append({
                    'name': pg['date'],
                    'value': [pg['date']+" 14:00:00", pg['p2hpg_noon']]
                })
                p2hpg_list.append({
                    'name': pg['date'],
                    'value': [pg['date']+" 20:00:00", pg['p2hpg_evening']]
                })



            return jsonify({
                'message': 'ok',
                'count': count,
                'fpg_list': fpg_list,
                'p2hpg_list': p2hpg_list
            }), 200
        else:
            return jsonify({'message': "error"}), 500
    except:
        return jsonify({'message': "bad arguments"}), 400

