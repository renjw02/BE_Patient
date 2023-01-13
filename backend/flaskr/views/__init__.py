# -*- coding: utf-8 -*-
from . import user, post, pg, log, favorite, news

# user post service
blueprints = [
    user.bp,
    post.bp,
    pg.bp,
    log.bp,
    favorite.bp,
    news.bp
]

def config_blueprint(app):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)