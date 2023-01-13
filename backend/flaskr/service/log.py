#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib
import datetime

from sqlalchemy import and_

from flaskr.models import Log
from flaskr.extensions import db

class LogService():
    
    def create_log(self, user_id, title, content, date):
        try:
            now = datetime.datetime.now()
            if date == 0:
                # date 是字符串
                date = datetime.date.today().isoformat()
            
            l = Log(user_id=user_id, title=title, content=content, date=date, created=now, updated=now)
            db.session.add(l)
            db.session.commit()
            return l, True
        except Exception as e:
            print(e)
            return "error", False
            

    def get_log(self, user_id, date):
        try:
            l = Log.query.filter(and_(Log.user_id == user_id, Log.date == date)).first()
            return l, True
        except Exception as e:
            print(e)
            return "error", False

    def update_log(self, log_id, title, content):
        try:
            now = datetime.datetime.now()
            db.session.query(Log).filter(Log.id == log_id).update({
                'title': title,
                'content': content,
                'updated': now
            })
            db.session.commit()
            return "ok", True
        except Exception as e:
            print(e)
            db.session.rollback()
            return "error", False
        

    def check_log(self, user_id, log_id):
        try:
            l = Log.query.filter(Log.id == log_id).first()
            if l.user_id == int(user_id):
                return True
            return False
        except Exception as e:
            print(e)
            return False