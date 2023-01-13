#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib
import datetime
from sqlalchemy import and_

from flaskr.extensions import db
from flaskr.models import Post, Reply

class PostService():
    
    def create_post(self, title, content, user_id):
        try:
            now = datetime.datetime.now()
            p = Post(user_id=user_id, title=title, content=content, favor_num=0, last_replied_user_id=user_id,
                    last_replied_time=now, created=now, updated=now)
            db.session.add(p)
            db.session.commit()
            return p, True
        except Exception as e:
            print(e)
            return "error", False

    def update_post(self, title, content, post_id, user_id):
        try:
            now = datetime.datetime.now()
            db.session.query(Post).filter(and_(Post.id == post_id, Post.user_id == user_id)).update({
                "title": title,
                "content": content,
                "updated": now
            })
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    def delete_post(self, post_id):
        try:
            db.session.query(Post).filter(Post.id == post_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    # 回复的是一个帖子，则不传入reply_id
    # reply_id: 将要回复的是一个reply，其id为reply_id
    def create_reply(self, content, user_id, post_id, reply_id=0):
        try:
            now = datetime.datetime.now()
            r = Reply(user_id=user_id, content=content, favor_num=0, post_id=post_id,
                    reply_id=reply_id, created=now, updated=now)
            db.session.add(r)
            db.session.query(Post).filter(Post.id == post_id).update({
                "last_replied_time": now,
                "last_replied_user_id": user_id,
            })
            db.session.commit()
            return r, True
        except Exception as e:
            db.session.rollback()
            print(e)
            return "error", False

    def update_reply(self, content, user_id, post_id, reply_id):
        try:
            now = datetime.datetime.now()
            db.session.query(Reply).filter(and_(Reply.id == reply_id, Reply.user_id == user_id)).update({
                "content": content,
                "updated": now
            })
            db.session.query(Post).filter(Post.id == post_id).update({
                "last_replied_time": now,
                "last_replied_user_id": user_id,
            })
            db.session.commit()
            return True
        except Exception as e:
            # 失败了之后事务回滚
            db.session.rollback()
            print(e)
            return False

    def delete_reply(self, reply_id):
        try:
            db.session.query(Reply).filter(Reply.id == reply_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False


    # 默认按帖子更新时间排序
    def get_post_list(self, user_id=0, page=1, size=10, order_by_reply=False):
        try:
            if order_by_reply:
                order_col = "post.last_replied_time"
            else:
                order_col = "post.updated"

            if user_id == 0:
                where_clause = ""
            else:
                where_clause = "where post.user_id = " + str(user_id)

            content_base = '''
                select
                    post.id as id, post.user_id as userId, create_user.nickname as nickname,
                    post.title as title, post.content as content, post.favor_num as favor_num,
                    post.last_replied_user_id as lastRepliedUserId,
                    reply_user.nickname as lastRepliedNickname,
                    post.last_replied_time as lastRepliedTime,
                    post.created as created, post.updated as updated
                from
                    post
                inner join user as create_user on post.user_id = create_user.id
                inner join user as reply_user on post.last_replied_user_id = reply_user.id
                {where}
                order by {order} desc
                limit {limit}
                offset {offset};
            '''
            count_base = '''
                select
                    count(post.id) as count
                from
                    post
                {where}
            '''
            sql_content = content_base.format(limit=size, offset=(
                page-1)*size, order=order_col, where=where_clause)
            sql_count = count_base.format(where=where_clause)

            content_result = db.session.execute(sql_content)
            count_result = db.session.execute(sql_count)

            post_list = [dict(zip(result.keys(), result))
                         for result in content_result]
            count = [dict(zip(result.keys(), result))
                     for result in count_result]

            return post_list, count[0]['count'], True
        except Exception as e:
            print(e)
            return [], 0, False
    
    def check_post(self, post_id, user_id):
        try:
            p = Post.query.filter(Post.id == post_id).first()
            if p.user_id == int(user_id):
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def check_reply(self, post_id, reply_id):
        try:
            if reply_id == 0:
                p = Post.query.filter(Post.id == post_id).first()
                if p is None:
                    return False
                else:
                    return True
            else:
                r = Reply.query.filter(Reply.id == reply_id).first()
                if r.post_id == int(post_id):
                    return True
                else:
                    return False
        except Exception as e:
            print(e)
            return False

    def check_self_reply(self, reply_id, user_id):
        try:
            r = Reply.query.filter(Reply.id == reply_id).first()
            if r.user_id == int(user_id):
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def get_post_detail(self, post_id):
        try:
            post_sql = '''
                select
                    post.id as id, post.user_id as userId, user.nickname as nickname,
                    post.title as title, post.content as content, post.favor_num as favor_num,
                    post.created as created, post.updated as updated, 
                    post.Last_replied_time as lastRepliedTime
                from
                    post
                inner join user on post.user_id = user.id
                where
                    post.id = {post_id};
            '''
            reply_sql = '''
                select
                    reply.id as id, reply.user_id as userId, user.nickname as nickname,
                    reply.post_id as postId, reply.reply_id as replyId,
                    reply.content as content, reply.favor_num as favor_num, 
                    reply.created as created, reply.updated as updated
                from
                    reply
                inner join user on reply.user_id = user.id
                where
                    reply.post_id = {post_id}
                order by reply.created asc;
            '''
            post_result = db.session.execute(post_sql.format(post_id=post_id))
            reply_result = db.session.execute(reply_sql.format(post_id=post_id))

            post = [dict(zip(result.keys(), result))
                    for result in post_result][0]
            reply_list = [dict(zip(result.keys(), result))
                          for result in reply_result]

            # reply列表包括帖子底下所有的回复，包括对帖子和对回复的
            post['reply'] = reply_list
            '''
            post = {
                'id':
                'userId":
                'nickname':
                'title':
                'content':
                'favor_num':
                'created':
                'updated':
                'lastRepliedTime':
                'reply':
            }
            '''
            return post, True
        except Exception as e:
            print(e)
            return None, False


    def get_reply(self, reply_id):
        try:
            r = Reply.query.filter(Reply.id == reply_id).first()
            return r, True
        except Exception as e:
            print(e)
            return 'errors', False

    def get_reply_list(self, reply_id):
        try:
            reply_sql = '''
                select
                    reply.id as id, reply.user_id as userId, user.nickname as nickname,
                    reply.post_id as postId, reply.reply_id as replyId,
                    reply.content as content, reply.favor_num as favor_num, 
                    reply.created as created, reply.updated as updated
                from
                    reply
                inner join user on reply.user_id = user.id
                where
                    reply.reply_id = {reply_id}
                order by reply.created asc;
            '''
            reply_result = db.session.execute(reply_sql.format(reply_id=reply_id))
            reply_list = [dict(zip(result.keys(), result)) for result in reply_result]
            return reply_list, True
        except Exception as e:
            print(e)

            return [], False


    def support_post(self, post_id, type):
        try:
            now = datetime.datetime.now()
            db.session.query(Post).filter(Post.id == post_id).update({
                "favor_num": Post.favor_num+type,
                "updated": now
            })
            db.session.commit()
            return 'ok', True
        except Exception as e:
            print(e)
            db.session.rollback()
            return 'errors', False

    
    def support_reply(self, reply_id, type):
        try:
            now = datetime.datetime.now()
            db.session.query(Reply).filter(Reply.id == reply_id).update({
                "favor_num": Reply.favor_num+type,
                "updated": now
            })
            db.session.commit()
            return 'ok', True
        except Exception as e:
            print(e)
            db.session.rollback()
            return 'errors', False