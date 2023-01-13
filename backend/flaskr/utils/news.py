#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib


import requests
import re
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin

# sys.path.append("..")

# os.chdir(sys.path[0])

html_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
{article}
</body>
</html>
"""

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"
]

class NewsSearch():

    def __init__(self):
        self.headers = {
            'user-agent':random.choice(USER_AGENT_LIST)
        }

    def search_jitang(self, pageNum, newsNum):#爬取鸡汤文 其中pageNUm必须大于等于2
        try:
            for page in range(2,pageNum+1):
                url = f'https://www.xinlizhi.cn/lzgushi/index_{page}.html'
                headers = self.headers
                try:
                    res = requests.get(url = url, headers = headers)
                    res.encoding = res.apparent_encoding
                    html = res.text
                    soup = BeautifulSoup(html,'html5lib')
                    newslist = soup.find_all(class_='e2')
                    for li in newslist:
                        if newsNum > 0:
                            title = li.find(class_='title').get_text()
                            link = li.a.attrs['href']
                            link = 'https://www.xinlizhi.cn'+link
                            self.news_html_spider(link,title,1)
                            newsNum = newsNum - 1
                        else :
                            break
                except Exception as e:
                    print(e)
                    continue
        except Exception as e:
            print(e)
            return False

    def parse_jitang_detail(self,response,link,title,category): #解析鸡汤文网页
        try:
            html = response.text
            new_title = "".join(title.split())
            soup = BeautifulSoup(html,'html5lib')
            content = soup.find(class_=['content'])
            html = html_str.format(article=content)
            absolutize = lambda m: ' src="' + urljoin(link, m.group(1)) + '"'
            html = re.sub(r' src="([^"]+)"', absolutize, html)#图片相对路径改为绝对路径
            self.write_content(html, new_title,category)
            return new_title
        except Exception as e:
            print(e)
            return False

    def search_changshi(self, pageNum, newsNum):#爬取糖尿病常识
        try:
            for page in range(2,pageNum+1):
                url = f'http://www.tnbzy.com/html/lada/knowledge/{page}.html'
                headers = self.headers
                try:
                    res = requests.get(url = url, headers = headers)
                    res.encoding = res.apparent_encoding
                    html = res.text
                    soup = BeautifulSoup(html,'html5lib')
                    newslist = soup.find_all(class_='col-md-8')
                    for li in newslist:
                        if newsNum > 0:
                            title = li.find(class_='black list_title').get_text()
                            link = li.a.attrs['href']
                            self.news_html_spider(link,title,2)
                            newsNum = newsNum - 1
                        else :
                            break
                except Exception as e:
                    print(e)
                    continue
        except Exception as e:
            print(e)
            return False

    def parse_changshi_detail(self,response,link,title,category): #解析糖尿病常识网页
        try:
            html = response.text
            new_title = "".join(title.split())
            soup = BeautifulSoup(html,'html5lib')
            content = soup.find(class_='textcontent')
            html = html_str.format(article=content)
            absolutize = lambda m: ' src="' + urljoin(link, m.group(1)) + '"'
            html = re.sub(r' src="([^"]+)"', absolutize, html)#图片相对路径改为绝对路径
            self.write_content(html, new_title,category)
            return new_title
        except Exception as e:
            print(e)
            return False

    def search_sina(self, pageNum, newsNum):#爬取糖尿病新闻 新浪
        try:
            for page in range(2,pageNum+1):
                url = f'https://search.sina.com.cn/news/?c=news&q=%E7%B3%96%E5%B0%BF%E7%97%85&col=&range=all&size=10&page={page}'
                headers = self.headers
                try:
                    res = requests.get(url = url, headers = headers)
                    res.encoding = res.apparent_encoding
                    html = res.text
                    soup = BeautifulSoup(html,'html5lib')
                    newslist = soup.find_all(class_='box-result clearfix')
                    for li in newslist:
                        if newsNum > 0:
                            title = li.find('a').get_text()
                            link = li.a.attrs['href']
                            title = self.news_html_spider(link,title,3)
                            newsNum = newsNum - 1
                        else :
                            break
                except Exception as e:
                    print(e)
                    continue
        except Exception as e:
            print(e)
            return False

    def parse_sina_detail(self,response,link,title,category): #解析新闻网页 新浪
        try:
            html = response.text
            new_title = "".join(title.split())
            soup = BeautifulSoup(html,'html5lib')
            content = soup.find(class_='article')
            for i in content.find_all(class_='article-notice'):
                i.decompose()
            html = html_str.format(article=content)
            absolutize = lambda m: ' src="' + urljoin(link, m.group(1)) + '"'
            html = re.sub(r' src="([^"]+)"', absolutize, html)#图片相对路径改为绝对路径
            self.write_content(html, new_title,category)
            return new_title
        except Exception as e:
            print(e)
            return False

    def search_yongyao(self, pageNum, newsNum):#爬取糖尿病用药
        try:
            for page in range(2,pageNum+1):
                url = f'http://www.tnbzy.com/html/lada/cure/{page}.html'
                headers = self.headers
                try:
                    res = requests.get(url = url, headers = headers)
                    res.encoding = res.apparent_encoding
                    html = res.text
                    soup = BeautifulSoup(html,'html5lib')
                    newslist = soup.find_all(class_='col-md-8')
                    for li in newslist:
                        if newsNum > 0:
                            title = li.find(class_='black list_title').get_text()
                            link = li.a.attrs['href']
                            self.news_html_spider(link,title,4)
                            newsNum = newsNum - 1
                        else :
                            break
                except Exception as e:
                    print(e)
                    continue
        except Exception as e:
            print(e)
            return False

    def parse_yongyao_detail(self,response,link,title,category): #解析糖尿病用药网页
        try:
            html = response.text
            new_title = "".join(title.split())
            soup = BeautifulSoup(html,'html5lib')
            content = soup.find(class_='textcontent')
            html = html_str.format(article=content)
            absolutize = lambda m: ' src="' + urljoin(link, m.group(1)) + '"'
            html = re.sub(r' src="([^"]+)"', absolutize, html)#图片相对路径改为绝对路径
            self.write_content(html, new_title,category)
            return new_title
        except Exception as e:
            print(e)
            return False

    def news_html_spider(self,link,title,category):
        try:
            if (category == 1):
                response = self.send_request(link)
                if response:
                    title = self.parse_jitang_detail(response,link,title,category)
            if (category == 2):
                response = self.send_request(link)
                if response:
                    title = self.parse_changshi_detail(response,link,title,category)
            if (category == 3):
                response = self.send_request(link)
                if response:
                    title = self.parse_sina_detail(response,link,title,category)
            if (category == 4):
                response = self.send_request(link)
                if response:
                    title = self.parse_yongyao_detail(response,link,title,category)
            return title
        except Exception as e:
            print(e)
            return False

    def send_request(self,url):
        try:
            response = requests.get(url=url,headers=self.headers)
            response.encoding = response.apparent_encoding  
            if response.status_code == 200:
                return response
        except Exception as e:
            print(e)
            return "errors", False

    def write_content(self,content, name, category):
        try:
            if (category == 1): #鸡汤
                name = name.replace(u'\xa0', u'')
                name = name.replace(u'|', u' ')
                content = content.replace(u'\xa0', u'')
                static_address = r'../static/news/type1/'+name+'.html'
                fp = open(static_address,'w',encoding='utf=8')
                fp.write(content)
            if (category == 2): #常识
                name = name.replace(u'\xa0', u'')
                name = name.replace(u'|', u' ')
                content = content.replace(u'\xa0', u'')
                static_address = r'../static/news/type2/'+name+'.html'
                fp = open(static_address,'w',encoding='utf=8')
                fp.write(content)
            if (category == 3): #新闻
                name = name.replace(u'\xa0', u'')
                name = name.replace(u'|', u' ')
                content = content.replace(u'\xa0', u'')
                static_address = r'../static/news/type3/'+name+'.html'
                fp = open(static_address,'w',encoding='utf=8')
                fp.write(content)
            if (category == 4): #用药
                name = name.replace(u'\xa0', u'')
                name = name.replace(u'|', u' ')
                content = content.replace(u'\xa0', u'')
                static_address = r'../static/news/type4/'+name+'.html'
                fp = open(static_address,'w',encoding='utf=8')
                fp.write(content)
        except Exception as e:
            print(1, e)
            return False

    def start(self):
        try:
            self.search_jitang(4,30)
            self.search_changshi(2,30)
            self.search_sina(5,30)
            self.search_yongyao(2,30)
        except Exception as e:
            print(e, 12)
            return False

    def getNewNews(self, newsNum=5):
        try:
            url = f'https://search.sina.com.cn/news/?c=news&q=%E7%B3%96%E5%B0%BF%E7%97%85&col=&range=all&size=10&page=1'
            headers = self.headers

            title_list = []

            try:
                res = requests.get(url = url, headers = headers)
                res.encoding = res.apparent_encoding
                html = res.text
                soup = BeautifulSoup(html,'html5lib')
                newslist = soup.find_all(class_='box-result clearfix')
                for li in newslist:
                    if newsNum > 0:
                        title = li.find('a').get_text()
                        link = li.a.attrs['href']
                        response = self.send_request(link)
                        if response:
                            html = response.text
                            title = "".join(title.split())
                            soup = BeautifulSoup(html,'html5lib')
                            content = soup.find(class_='article')
                            for i in content.find_all(class_='article-notice'):
                                i.decompose()
                            html = html_str.format(article=content)
                            absolutize = lambda m: ' src="' + urljoin(link, m.group(1)) + '"'
                            html = re.sub(r' src="([^"]+)"', absolutize, html)#图片相对路径改为绝对路径
                            # self.write_content(html, title, 3)
                            title = title.replace(u'\xa0', u'')
                            title = title.replace(u'|', u' ')
                            content = html.replace(u'\xa0', u'')
                            # static_address = r'../static/news/type3/'+title+'.html'
                            static_address = r'./flaskr/static/news/type3/'+title+'.html'
                            fp = open(static_address,'w',encoding='utf=8')
                            fp.write(content)

                        title_list.append(title)

                        newsNum = newsNum - 1
                    else :
                        break
                
                return title_list, True
            except Exception as e:
                print(e)
                return [], False
        except Exception as e:
            print(e)
            return [], False


if __name__ == '__main__':
    temp = NewsSearch()
    temp.start()
    # t, f = temp.getNewNews()
    # print(t)