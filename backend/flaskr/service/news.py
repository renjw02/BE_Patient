#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib

from sqlalchemy import and_

from flaskr.models import News
from flaskr.extensions import db

class NewsService():

    def create_news(self, title, address, keyword, date):
        try:
            n = News(title=title,address=address,keyword=keyword,date=date)
            db.session.add(n)
            db.session.commit()
            return n,True
        except Exception as e:
            print(e)
            return "error", False

    def get_news(self,id):
        try:
            n = News.query.filter(and_(News.id == id)).first()
            return n, True
        except Exception as e:
            print(e)
            return "error", False

    def get_news_list(self,page=1,size=10,keyword=0):
        try:
            order_col = "news.id"
            if keyword == 0:
                where_clause = ""
            else:
                where_clause = "where news.keyword = " + str(keyword)
            content_base = '''
                select
                    news.id as id, news.title as title, news.address as address,
                    news.keyword as keyword, news.date as date
                from
                    news
                {where}
                order by {order} desc
                limit {limit}
                offset {offset};
            '''
            count_base = '''
                select
                    count(news.id) as count
                from
                    news
                {where}
            '''
            sql_content = content_base.format(limit=size, offset=(
                page-1)*size, where=where_clause, order=order_col)
            sql_count = count_base.format(where=where_clause)

            content_result = db.session.execute(sql_content)
            count_result = db.session.execute(sql_count)

            news_list = [dict(zip(result.keys(), result))
                         for result in content_result]
            count = [dict(zip(result.keys(), result))
                     for result in count_result]

            return news_list, count[0]['count'], True
        except Exception as e:
            print(e)
            return [], 0, False


    def get_news_list_by_search(self, word, page=1):
        try:
            where_clause = "where news.title like '%" + str(word) + "%'"
            size = 10
            order_col = "news.id"

            content_base = '''
                select
                    news.id as id, news.title as title, news.address as address,
                    news.keyword as keyword, news.date as date
                from
                    news
                {where}
                limit {limit}
                offset {offset};
            '''
            count_base = '''
                select
                    count(news.id) as count
                from
                    news
                {where}
            '''
            sql_content = content_base.format(limit=size, offset=(
                page-1)*size, where=where_clause, order=order_col)
            sql_count = count_base.format(where=where_clause)

            content_result = db.session.execute(sql_content)
            count_result = db.session.execute(sql_count)

            news_list = [dict(zip(result.keys(), result))
                         for result in content_result]
            count = [dict(zip(result.keys(), result))
                     for result in count_result]

            return news_list, count[0]['count'], True
        except Exception as e:
            print(e)
            return [], 0, False
