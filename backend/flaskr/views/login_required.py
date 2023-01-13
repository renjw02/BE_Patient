#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib
from flask import g

# 前端传入信息应该包含jwt
def login_required(func):
    """
    用户必须登录装饰器
    使用方法：放在 method_decorators 中
    """
    # @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.user_id:
            return {'message': 'User must be authorized.'}, 401
        else:
            return func(*args, **kwargs)
    wrapper.__name__ = "warper" + func.__name__
    return wrapper
