#!/usr/bin/env python

__author__ = 'SLZ'

'''
articles controller.
'''
import time

from digwebs.web import current_app, ctx
import markdown2
from model.in_memory_db import get_time_stamp, list_simple_articles, get_single_article, get_near_articles, delete_article, update_single_article, add_article

@current_app.view('blogs.html')
@current_app.get('/views/blogs')
def blogs():
    number_of_articles_per_page = 2
    i = ctx.request.input()
    r = i.get('current_page_no', '')
    if not r:
        next_articles = list_simple_articles(True, get_time_stamp(0), number_of_articles_per_page)
        current_page_no = 1
    else:
        current_page_no = int(i.get('current_page_no').strip())
        is_next = int(i.get('is_next', '1').strip()) == 1
        created_timestamp = int(i.get('created_timestamp').strip())
        next_articles = list_simple_articles(is_next, created_timestamp, number_of_articles_per_page)
    return dict(template_blogs=next_articles, number_of_total_pages = 0, current_page_no = current_page_no)

@current_app.view('single_article.html')
@current_app.get('/views/article/:id')
def view_article(id):
    real_id = int(id)
    article = get_single_article(real_id)
    near_articles = get_near_articles(real_id)
    return dict(
        article_content = markdown2.markdown(article['markdown_content']),
        article = article,
        newer_article = near_articles[0],
        older_article = near_articles[1]
        )

@current_app.api
@current_app.delete('/manage/api/v1/article')
def handle_delete():
    i = ctx.request.input()
    real_id = int(i.get('id').strip())
    a = delete_article(real_id)
    return dict(successed=a is not None)

@current_app.view('edit-article.html')
@current_app.get('/manage/views/article')
def handle_edit():
    i = ctx.request.input()
    real_id = i.get('id',"").strip()
    if real_id:
        real_id = int(real_id)
        article = get_single_article(real_id)
        return dict(article=article)
    return dict(article=dict())

@current_app.api
@current_app.put('/manage/api/v1/article')
def handle_modify():
    i = ctx.request.input()
    real_id = i.get('id',"").strip()
    title = i.get('title',"").strip()
    description = i.get('description',"").strip()
    markdown_content = i.get('markdown_content',"").strip()
    real_id = int(real_id)
    article = update_single_article(id=real_id,title=title,description=description,markdown_content=markdown_content)
    return dict(successed=1,id=real_id)

@current_app.api
@current_app.post('/manage/api/v1/article')
def handle_add():
    i = ctx.request.input()
    title = i.get('title',"").strip()
    description = i.get('description',"").strip()
    markdown_content = i.get('markdown_content',"").strip()
    new_article = add_article(title=title,
    description=description,
    markdown_content=markdown_content,
    created_date=time.time(),
    author_name=ctx.request.user_name)
    return dict(successed=1,id=new_article['id'])