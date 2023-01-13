# -*- coding: utf-8 -*-

from flaskr.extensions import db


class User(db.Model):
    """
    论坛用户
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, doc="用户id")

    username = db.Column(db.String(32), unique=True, doc="账号")
    password = db.Column(db.String(255), doc="密码")
    nickname = db.Column(db.String(255), doc="用户名称")

    status = db.Column(db.Integer, doc="登录状态")

    mobile = db.Column(db.String(255), doc="手机号")
    address = db.Column(db.String(255), doc="个人地址")
    signature = db.Column(db.String(255), doc="个性签名")

    created = db.Column(db.DateTime, doc="创建时间")
    updated = db.Column(db.DateTime, doc="更新时间")


# max size of content: 1024
class Post(db.Model):
    """
    帖子
    """
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, doc="帖子id")

    user_id = db.Column(db.Integer, doc="发帖用户id")

    title = db.Column(db.String(255), doc="帖子标题")
    content = db.Column(db.String(1024), doc="帖子内容")

    favor_num = db.Column(db.Integer, doc="点赞数目")

    last_replied_user_id = db.Column(db.Integer, doc="最新回复的用户id")
    last_replied_time = db.Column(db.DateTime, doc="最新回复时间")

    created = db.Column(db.DateTime, doc="创建时间")
    updated = db.Column(db.DateTime, doc="更新时间")


# max size of content: 1024
class Reply(db.Model):
    """
    回复
    """
    __tablename__ = 'reply'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, doc="回复id")

    user_id = db.Column(db.Integer, doc="回复用户id")

    post_id = db.Column(db.Integer, doc="回复帖子id")       # reply a post
    reply_id = db.Column(db.Integer, doc="回复回复id")      # reply a reply in a post

    content = db.Column(db.String(1024), doc="回复内容")

    favor_num = db.Column(db.Integer, doc="点赞数目")

    created = db.Column(db.DateTime, doc="创建时间")
    updated = db.Column(db.DateTime, doc="更新时间")


class PG(db.Model):
    """
    血糖
    """
    __tablename__ = 'pg'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, doc="血糖id")

    date = db.Column(db.String(128), doc="血糖日期")
    user_id = db.Column(db.Integer, doc="用户id")

    fpg_morning = db.Column(db.Float, doc="早上fpg")
    fpg_noon = db.Column(db.Float, doc="中午fpg")
    fpg_evening = db.Column(db.Float, doc="晚上fpg")
    p2hpg_morning = db.Column(db.Float, doc="早上p2hpg")
    p2hpg_noon = db.Column(db.Float, doc="中午p2hpg")
    p2hpg_evening = db.Column(db.Float, doc="晚上p2hpg")
    

    created = db.Column(db.DateTime, doc="创建时间")
    updated = db.Column(db.DateTime, doc="更新时间")



class Log(db.Model):
    """
    用户日志
    """
    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, doc="日志id")

    user_id = db.Column(db.Integer, doc="用户id")
    
    title = db.Column(db.String(255), doc="日志标题")
    content = db.Column(db.String(1024), doc="日志内容")

    date = db.Column(db.String(128), unique=True, doc="日志日期")

    created = db.Column(db.DateTime, doc="创建时间")
    updated = db.Column(db.DateTime, doc="更新时间")


class Favorite(db.Model):
    """
    收藏
    """
    __tablename__ = 'favorite'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, doc="收藏id")

    user_id = db.Column(db.Integer, doc="用户id")
    post_id = db.Column(db.Integer, doc="帖子id")
    news_id = db.Column(db.Integer, doc="资讯id")
    
    title = db.Column(db.String(255), doc="标题")




class News(db.Model):
    """
    资讯系统
    """
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, doc="资讯id")

    title = db.Column(db.String(255), doc="资讯标题")
    address = db.Column(db.String(255), unique=True, doc="资讯地址")

    keyword = db.Column(db.Integer, doc="关键词")

    date = db.Column(db.String(128), doc="资讯日期")