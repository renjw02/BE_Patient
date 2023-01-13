#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib
import os
import unittest
import coverage
import datetime

from flaskr import create_app, db, aps
from flaskr.models.model import User
from flaskr.utils import encrypt_password, config, NewsSearch

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from flaskr.service import NewsService

app = create_app(os.getenv('TYPE', 'default'))
aps.start()

manager = Manager(app)
migrate = Migrate(app, db)
host = config.get_yaml('app.HOST')
port = config.get_yaml('app.PORT')

manager.add_command('runserver', Server(host=host, port=port))
manager.add_command('db', MigrateCommand)

@manager.command
def test(filter=None):
    """Run the unit tests"""
    COV = coverage.coverage(branch=True, include='flaskr/*')
    COV.start()
    loader = unittest.TestLoader()
    loader.testNamePatterns = [filter+"*"] if filter is not None else None
    tests = loader.discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    COV.stop()
    COV.save()
    print('Coverage:')
    COV.report()
    basedir = os.path.abspath(os.path.dirname("backend"))
    covdir = os.path.join(basedir, 'test_report')
    COV.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)

@manager.command
def init_db():
    """Init db"""
    db.drop_all()
    db.create_all()
    me = User(username="test", password=encrypt_password(str("test")), nickname="test", mobile="45678901122")  
    db.session.add(me)
    db.session.commit()

@manager.command
def init_news():
    """Init news"""
    # geter = NewsSearch()
    # geter.start()

    now = datetime.datetime.now()
    service = NewsService()
    file_list = os.listdir("./flaskr/static/news/type1")
    for file in file_list:
        service.create_news(file[0:-5], "./flaskr/static/news/type1/"+str(file), 1, str(now))

    file_list = os.listdir("./flaskr/static/news/type2")
    for file in file_list:
        service.create_news(file[0:-5], "./flaskr/static/news/type2/"+str(file), 2, str(now))

    file_list = os.listdir("./flaskr/static/news/type3")
    for file in file_list:
        service.create_news(file[0:-5], "./flaskr/static/news/type3/"+str(file), 3, str(now))

    file_list = os.listdir("./flaskr/static/news/type4")
    for file in file_list:
        service.create_news(file[0:-5], "./flaskr/static/news/type4/"+str(file), 4, str(now))

if __name__ == '__main__':
    manager.run()