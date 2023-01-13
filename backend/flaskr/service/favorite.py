#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib
from sqlalchemy import and_

from flaskr.models import Favorite
from flaskr.extensions import db

class FavoriteService():
    
    def create_favorite(self, user_id, post_id, news_id, title):
        try:
            f = Favorite(user_id=user_id, title=title, post_id=post_id, news_id=news_id)
            db.session.add(f)
            db.session.commit()
            return f, True
        except Exception as e:
            print(e)
            return "error", False
            

    def delete_favorite(self, favorite_id):
        try:
            db.session.query(Favorite).filter(Favorite.id == favorite_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
    

    def get_fav_list(self, user_id, page=1, type=0):
        try:
            size = 10
            where_clause = "where favorite.user_id = " + str(user_id)
            if type == 1:
                # post
                where_clause += " and favorite.news_id = 0"
            elif type == 2:
                # news
                where_clause += " and favorite.post_id = 0"

            content_base = '''
                select
                    favorite.id as id, favorite.user_id as userId, favorite.post_id as postId,
                    favorite.news_id as newsId, favorite.title as title
                from
                    favorite
                {where}
                limit {limit}
                offset {offset};
            '''
            count_base = '''
                select
                    count(favorite.id) as count
                from
                    favorite
                {where}
            '''
            sql_content = content_base.format(limit=size, offset=(
                page-1)*size, where=where_clause)
            sql_count = count_base.format(where=where_clause)

            content_result = db.session.execute(sql_content)
            count_result = db.session.execute(sql_count)

            favorite_list = [dict(zip(result.keys(), result)) for result in content_result]
            count = [dict(zip(result.keys(), result)) for result in count_result]

            return favorite_list, count[0]['count'], True
        except Exception as e:
            print(e)
            return [], 0, False
        
    # 提供user_id和post_id,查找有无收藏
    def check_favorite_post(self, user_id, post_id):
        try:
            f = Favorite.query.filter(and_(Favorite.user_id == user_id, Favorite.post_id == post_id)).first()
            if f is None:
                return 'error', False
            return f, True
        except Exception as e:
            print(e)
            return 'error', False

    
    def check_favorite_news(self, user_id, news_id):
        try:
            f = Favorite.query.filter(and_(Favorite.user_id == user_id, Favorite.news_id == news_id)).first()
            if f is None:
                return 'error', False
            return f, True
        except Exception as e:
            print(e)
            return 'error', False


    def check_favor(self, user_id, favor_id):
        try:
            f = Favorite.query.filter(Favorite.id == favor_id).first()
            if f.user_id == int(user_id):
                return True
            return False
        except Exception as e:
            print(e)
            return False