#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib
import os, datetime

from flask import Flask
from flask_cors import CORS


from flaskr.configs import configs
from flaskr.extensions import db, aps
from flaskr.views import config_blueprint
from flaskr.utils import jwt_authentication, NewsSearch
from flaskr.service import NewsService


def get_news_task(app):
    print("It's time to get news!")
    temp = NewsSearch()
    title_list, flag = temp.getNewNews()

    if flag:
     # add into db
        db.app = app
        print(title_list)
        for title in title_list:
            path = r'./static/news/type3/'+title+'.html'
            now = datetime.datetime.now()
            creator = NewsService()
            creator.create_news(title, path, 3, str(now))
    else:
        print("get failed")




def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    if test_config is None:
        test_config = os.getenv('TYPE', 'default')
    
    app.config.from_object(configs[test_config])
    app.before_request(jwt_authentication)

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    # blueprints
    config_blueprint(app)

    # db
    db.init_app(app)

    # aps
    aps.init_app(app)
    aps.add_job(id='grab', timezone='Asia/Shanghai', func=get_news_task, args=(app,),
        trigger="cron", day_of_week="0-6", hour=9)
    # aps.add_job(id='test', func=task, args=(1,2), trigger="interval", seconds=5)

    return app


if __name__ == '__main__':
    get_news_task()