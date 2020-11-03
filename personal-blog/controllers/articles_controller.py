#!/usr/bin/env python

__author__ = 'SLZ'

'''
articles controller.
'''

from digwebs.web import current_app, ctx
import markdown2
from model.in_memory_db import list_simple_articles, get_single_article, get_near_articles

@current_app.view('blogs.html')
@current_app.get('/views/blogs')
def blogs():
    number_of_articles_per_page = 2
    i = ctx.request.input()
    current_page_no = int(i.get('current_page_no', '1').strip())
    total_articles = list_simple_articles()
    number_of_total_articles = len(total_articles)
    number_of_total_pages = int(number_of_total_articles / number_of_articles_per_page) + (number_of_total_articles % number_of_articles_per_page)
    if current_page_no < 1:
        current_page_no = 1
    elif current_page_no > number_of_total_pages:
        current_page_no = number_of_total_pages
    start_index = (current_page_no - 1) * number_of_articles_per_page
    end_index = start_index + number_of_articles_per_page
    if end_index > number_of_total_articles:
        end_index = start_index + (number_of_total_articles % number_of_articles_per_page)
    return dict(template_blogs=total_articles[start_index:end_index], number_of_total_pages = number_of_total_pages, current_page_no = current_page_no)

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