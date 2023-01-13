# -*- coding: utf-8 -*-
"""
Flask 扩展
"""
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

db = SQLAlchemy()
aps = APScheduler(scheduler=BackgroundScheduler())