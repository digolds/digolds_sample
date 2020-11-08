import time
import copy
import logging

from articles_content import internet_content, internet_description, internet_title

import boto3
from botocore.exceptions import ClientError

articles = dict()
'''
an article structure

{
    'title':'What is digwebs',
    'description':'A tiny web framework called digwebs which is developed by Python.',
    'markdown_content':'######',
    'created_date':1604282588, # int(time.time())
    'author_name':'slz',
    'id':9609923996892418
}
'''

def _generate_article(**kwargs):
    title = kwargs.get("title")
    description = kwargs.get("description")
    markdown_content = kwargs.get("markdown_content")
    created_date = kwargs.get("created_date")
    author_name = kwargs.get("author_name")
    a = {
        'title':title,
        'description':description,
        'markdown_content':markdown_content,
        'created_date':created_date, # int(time.time())
        'author_name':author_name,
        'id':hash(f'{author_name}-{created_date}') % (10 ** 16)
    }
    return a

def list_articles():
    simple_articles = []
    simple_articles = list(articles.items())
    def sort_by_created_date(e):
        return e[1]['created_date']
    simple_articles.sort(reverse=True, key=sort_by_created_date)
    return list(map(lambda x: x[1], simple_articles))

def list_simple_articles():
    detail_articles = list_articles()
    def filter_markdown_content(x):
        a = copy.deepcopy(x)
        del a['markdown_content']
        return a
    return list(map(filter_markdown_content, detail_articles))

dynamodb = None
def _dynamodb_service():
    global dynamodb
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    return dynamodb

def add_article(**kwargs):
    a = _generate_article(**kwargs)
    db = _dynamodb_service()
    table = db.Table('personal-articles-table')

    try:
        response = table.put_item(
            Item={
                'id': a.get("id"),
                'created_date': a.get("created_date"),
                'title': a.get("title"),
                'description': a.get("description"),
                'markdown_content': a.get("markdown_content"),
                'author_name': a.get("author_name"),
            }
        )
        logging.info(response)
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
        return None
    else:
        return a

def delete_article(id, created_date):
    db = _dynamodb_service()
    table = db.Table('personal-articles-table')
    try:
        response = table.delete_item(
            Key={
                'id': id,
                'created_date': created_date
            }
        )
    except ClientError as e:
        logging.info(e.response['Error']['Message'])
        return None
    else:
        logging.info(response)
        return response

def get_single_article(id, created_date):
    db = _dynamodb_service()
    table = db.Table('personal-articles-table')

    try:
        response = table.get_item(Key={'id': id, 'created_date': created_date})
        logging.info(response)
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
    else:
        return response['Item']

def update_single_article(**kwargs):
    db = _dynamodb_service()
    table = db.Table('personal-articles-table')
    response = table.update_item(
        Key={
            'id': kwargs.get("id"),
            'created_date': kwargs.get('created_date')
        },
        UpdateExpression="set title=:t, description=:d, markdown_content=:m",
        ExpressionAttributeValues={
            ':t': kwargs.get("title"),
            ':d': kwargs.get("description"),
            ':m': kwargs.get("markdown_content")
        },
        ReturnValues="UPDATED_NEW"
    )
    logging.info(response)
    return response['Attributes']

def get_near_articles(id):
    articles = list_articles()
    newer_index = -1
    older_index = -1
    found_index = -1
    for idx, a in enumerate(articles):
        if a['id'] == id:
            found_index = idx
            break
    newer_index = found_index - 1
    older_index = found_index + 1
    newer_article = None
    if newer_index > -1:
        newer_article = articles[newer_index]
    
    older_article = None
    if older_index < len(articles):
        older_article = articles[older_index]
    return (newer_article, older_article)

def _init_test_data():
    article_param = {
        'title':internet_title,
        'description':internet_description,
        'markdown_content':internet_content,
        'created_date':int(time.time()),
        'author_name':'slz'
    }
    
    a = _generate_article(**article_param)
    articles[a['id']] = a
    
    a = _generate_article(
        title="Why you should use digwebs?",
        description="Digwebs is a Python web framework, which you can use to accelerate the development process of building a web service.",
        markdown_content="# Why you should use digwebs?",
        created_date=int(time.time()) + 1,
        author_name='slz'
    )
    articles[a['id']] = a

    a = _generate_article(
        title="Where to learn programming?",
        description="Head to digolds.cn, it's a great place to share your idea!",
        markdown_content="# Hello Digolds!",
        created_date=int(time.time()) + 2,
        author_name='digolds'
    )
    articles[a['id']] = a
    return articles

#_init_test_data()

if __name__ == '__main__':
    # test initialization
    _init_test_data()
    assert(len(articles) == 3)
    
    # test sorted detail articles
    sorted_articles = list_articles()
    assert(len(sorted_articles) == 3)
    assert(sorted_articles[0]["created_date"] > sorted_articles[1]["created_date"])
    
    # test sorted simple articles
    sorted_simple_articles = list_simple_articles()
    assert(len(sorted_simple_articles) == 3)
    assert(sorted_simple_articles[0]["created_date"] > sorted_simple_articles[1]["created_date"])
    assert('markdown_content' not in sorted_simple_articles)

    # test add an article
    new_article = add_article(title="Where to learn programming?",
        description="Head to digolds.cn, it's a great place to share your idea!",
        markdown_content="# Hello Digolds!",
        created_date=int(time.time()) + 3,
        author_name='digolds')
    articles[new_article['id']] = new_article
    assert(len(articles) == 4)

    # test get an article
    new_article_copy = get_single_article(new_article['id'], new_article['created_date'])
    assert(new_article_copy['created_date'] == new_article['created_date'])
    
    # test update an article
    changed_title = "Where to learn programming and design idea?"
    updated_article = update_single_article(
        id = new_article["id"],
        title = changed_title,
        description=new_article['description'],
        markdown_content=new_article["markdown_content"],
        created_date=new_article['created_date'],
        author_name=new_article['author_name']
    )
    assert(updated_article['title'] == changed_title)

    # test delete an article
    deleted_article = delete_article(new_article['id'], new_article['created_date'])
    assert(len(articles) == 4)