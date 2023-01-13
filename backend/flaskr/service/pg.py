#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib
import datetime
from sqlalchemy import and_

from flaskr.models import PG
from flaskr.extensions import db

class pgService():
    
    def create_pg(self, user_id, date, fpg_morning=0, fpg_noon=0, 
                        fpg_evening=0, p2hpg_morning=0, p2hpg_noon=0, p2hpg_evening=0):
        try:
            # date 2017-12-20
            now = datetime.datetime.now()
            if date == 0:
                # date 是字符串
                date = datetime.date.today().isoformat()

            tmp = PG.query.filter(and_(PG.user_id == user_id, PG.date == date)).first()
            if tmp is not None:
                return "wrong date", False

            f = PG(user_id=user_id, fpg_morning=float(fpg_morning), fpg_noon=float(fpg_noon), 
                        fpg_evening=float(fpg_evening), p2hpg_morning=float(p2hpg_morning),
                        p2hpg_noon=float(p2hpg_noon), p2hpg_evening=float(p2hpg_evening), 
                        date=date, created=now, updated=now)
            db.session.add(f)
            db.session.commit()
            return f, True
        except Exception as e:
            print(e)
            return "error", False



    def update_pg(self, id, fpg_morning=0, fpg_noon=0, 
                        fpg_evening=0, p2hpg_morning=0, p2hpg_noon=0, p2hpg_evening=0):
        try:
            now = datetime.datetime.now()
            db.session.query(PG).filter(PG.id == id).update({
                'fpg_morning': fpg_morning,
                'fpg_noon': fpg_noon,
                'fpg_evening': fpg_evening,
                'p2hpg_morning': p2hpg_morning,
                'p2hpg_noon': p2hpg_noon,
                'p2hpg_evening': p2hpg_evening,
                'updated': now
                })
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False


    def check_pg(self, id ,user_id):
        try:
            p = PG.query.filter(PG.id == id).first()
            if p.user_id == int(user_id):
                return True
            return False
        except Exception as e:
            print(e)
            return False


    def get_pg(self, user_id, date):
        try:       
            date = "'" + date + "'"
            where_clause = "where pg.user_id = {id} and pg.date = {date}".format(id=user_id, date=str(date)) 
            # where_clause = "where fpg.user_id= {id}".format(id=user_id) 

            content_base = '''
                select
                    pg.id as id, pg.user_id as userId, pg.fpg_morning as fpg_morning,
                    pg.fpg_noon as fpg_noon, pg.fpg_evening as fpg_evening,
                    pg.p2hpg_morning as p2hpg_morning, pg.p2hpg_noon as p2hpg_noon,
                    pg.p2hpg_evening as p2hpg_evening, pg.date as date, pg.created as created, 
                    pg.updated as updated
                from
                    pg
                {where}
            '''

            sql_content = content_base.format(where=where_clause)
            content_result = db.session.execute(sql_content)
            pg = [dict(zip(result.keys(), result)) for result in content_result][0]
            
            return pg, True
        except Exception as e:
            print(e)
            return None, False


    def get_pg_list(self, user_id, page=1):
        try:
            size = 10
            where_clause = "where pg.user_id = " + str(user_id)
            order_col = "pg.date"

            content_base = '''
                select
                    pg.id as id, pg.user_id as userId, pg.fpg_morning as fpg_morning,
                    pg.fpg_noon as fpg_noon, pg.fpg_evening as fpg_evening,
                    pg.p2hpg_morning as p2hpg_morning, pg.p2hpg_noon as p2hpg_noon,
                    pg.p2hpg_evening as p2hpg_evening, pg.date as date, pg.created as created, 
                    pg.updated as updated
                from
                    pg
                {where}
                order by {order} desc
                limit {limit}
                offset {offset};
            '''
            count_base = '''
                select
                    count(pg.id) as count
                from
                    pg
                {where}
            '''
            sql_content = content_base.format(limit=size, offset=(
                page-1)*size, order=order_col, where=where_clause)
            sql_count = count_base.format(where=where_clause)

            content_result = db.session.execute(sql_content)
            count_result = db.session.execute(sql_count)

            pg_list = [dict(zip(result.keys(), result)) for result in content_result]
            count = [dict(zip(result.keys(), result)) for result in count_result]

            return pg_list, count[0]['count'], True
        except Exception as e:
            print(e)
            return [], 0, False


    def get_pg_all(self, user_id):
        try:
            where_clause = "where pg.user_id = " + str(user_id)
            order_col = "pg.date"

            content_base = '''
                select
                    pg.id as id, pg.user_id as userId, pg.fpg_morning as fpg_morning,
                    pg.fpg_noon as fpg_noon, pg.fpg_evening as fpg_evening,
                    pg.p2hpg_morning as p2hpg_morning, pg.p2hpg_noon as p2hpg_noon,
                    pg.p2hpg_evening as p2hpg_evening, pg.date as date, pg.created as created, 
                    pg.updated as updated
                from
                    pg
                {where}
                order by {order} asc
            '''
            count_base = '''
                select
                    count(pg.id) as count
                from
                    pg
                {where}
            '''
            sql_content = content_base.format(order=order_col, where=where_clause)
            sql_count = count_base.format(where=where_clause)

            content_result = db.session.execute(sql_content)
            count_result = db.session.execute(sql_count)

            pg_list = [dict(zip(result.keys(), result)) for result in content_result]
            count = [dict(zip(result.keys(), result)) for result in count_result]

            return pg_list, count[0]['count'], True
        except Exception as e:
            print(e)
            return [], 0, False