#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib


def favorite_params_check(content):
    '''
    post_id
    news_id
    '''
    if 'title' in content:
        pass
    else:
        return "title", False

    if 'post_id' in content:
        pass
    else:
        content['post_id'] = 0

    if 'news_id' in content:
        pass
    else:
        content['news_id'] = 0

    if content['post_id'] == 0 and content['news_id'] == 0:
        return "post_id and news_id", False
    
    return "ok", True
