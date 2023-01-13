#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib
import datetime

from sqlalchemy import and_

from flaskr.utils import encrypt_password
from flaskr.models import User
from flaskr.extensions import db

class UserService():
    ''' 
    accept a dictionary
    content = {
        'username':
        'password':
        'nickname':
        'mobile':
        'address':
        'signature':
    }
    '''

    def create_user(self, username, password, nickname, mobile, address, signature):
        try:
            now = datetime.datetime.now()
            pw = encrypt_password(str(password))

            u = User(username=username, password=pw, 
                    nickname=nickname,mobile=mobile, address=address, 
                    signature=signature, created=now, updated=now, status=0)
            db.session.add(u)
            db.session.commit()
            return u, True
        except Exception as e:
            print(e)
            return "error", False

    # return a tuple
    def get_user_by_id(self, user_id):
        try:
            u = User.query.filter(User.id == user_id).first()
            return u, True
        except Exception as e:
            print(e)
            return "errors", False

    # return a tuple
    def get_user_by_name_and_pass(self, username, password):
        try:
            pw = encrypt_password(str(password))
            u = User.query.filter(
                and_(User.username == username, User.password == pw)).first()
            # u = User.query.filter(User.password == pw).first()
            if u is None:
                return "not found", False
            return u, True
        except Exception as e:
            print(e)
            return "errors", False

    
    def change_attr(self, user_id, username, nickname, mobile, address, signature):
        try:
            now = datetime.datetime.now()
            db.session.query(User).filter(User.id == user_id).update({
                'username': username,
                'nickname': nickname,
                'mobile': mobile,
                'address': address,
                'signature': signature,
                'updated': now
            })
            u = User.query.filter(User.id == user_id).first()
            db.session.commit()
            return u, True
        except Exception as e:
            print(e)
            db.session.rollback()
            return '用户名已存在', False  


    def get_user(self, user_id):
        try:
            u = User.query.filter(User.id == user_id).first()
            return u, True
        except Exception as e:
            print(e)
            return "errors", False

    
    def reset_pw(self, username, mobile, password):
        try:
            pw = encrypt_password(password)
            db.session.query(User).filter(and_(User.username == username, User.mobile == mobile)).update({
                'password': pw
            })
            db.session.commit()
            u = User.query.filter(User.username == username).first()
            return u, True
        except Exception as e:
            print(e)
            db.session.rollback()
            return 'error', False 

    
    def login(self, user_id):
        try:
            db.session.query(User).filter(User.id == user_id).update({
                'status': 1
            })
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
        
    def logout(self, user_id):
        try:
            db.session.query(User).filter(User.id == user_id).update({
                'status': 0
            })
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
