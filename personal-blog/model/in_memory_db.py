import time
import copy
import logging
from datetime import datetime, timedelta

from model.articles_content import internet_content, internet_description, internet_title

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

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

def get_time_stamp(last_hours):
    last_x_hours_date_time = datetime.now() - timedelta(hours = last_hours)
    return int(last_x_hours_date_time.timestamp())

def list_simple_articles(go_next, start_time, articles_per_page):
    db = _dynamodb_service()
    table = db.Table('personal-articles-table')
    if go_next:
        sort_key_cond = Key('CreatedDateTime').lt(start_time)
    else:
        sort_key_cond = Key('CreatedDateTime').gt(start_time)

    response = table.query(
        IndexName='ContentGlobalIndex',
        KeyConditionExpression=Key('ContentType').eq(0) & sort_key_cond,
        Limit = articles_per_page,
        ScanIndexForward = not go_next
    )
    def filter_markdown_content(x):
        a = {}
        a['title'] = x['Title']
        a['description'] = x['Description']
        a['created_date'] = int(x['CreatedDateTime'])
        a['author_name'] = x['AuthorName']
        a['id'] = int(x['Id'])
        return a
    if go_next:
        return list(map(filter_markdown_content, response['Items']))
    else:
        tmp = list(map(filter_markdown_content, response['Items']))
        tmp.sort(reverse=True, key=lambda x: x['created_date'])
        return tmp

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
                'Id': a.get("id"),
                'ContentType': 0,
                'CreatedDateTime': a.get("created_date"),
                'Title': a.get("title"),
                'Description': a.get("description"),
                'MarkdownContent': a.get("markdown_content"),
                'AuthorName': a.get("author_name"),
            }
        )
        logging.info(response)
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
        return None
    else:
        return a

def delete_article(id):
    db = _dynamodb_service()
    table = db.Table('personal-articles-table')
    try:
        response = table.delete_item(
            Key={
                'Id': id
            }
        )
    except ClientError as e:
        logging.info(e.response['Error']['Message'])
        return None
    else:
        logging.info(response)
        return response

def get_single_article(id):
    db = _dynamodb_service()
    table = db.Table('personal-articles-table')

    try:
        response = table.get_item(Key={'Id': id})
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
            'Id': kwargs.get("id")
        },
        UpdateExpression="set Title=:t, Description=:d, MarkdownContent=:m",
        ExpressionAttributeValues={
            ':t': kwargs.get("title"),
            ':d': kwargs.get("description"),
            ':m': kwargs.get("markdown_content")
        },
        ReturnValues="UPDATED_NEW"
    )
    logging.info(response)
    return response['Attributes']

def get_near_articles(created_date):
    olders = list_simple_articles(True, created_date, 1)
    newers = list_simple_articles(False, created_date, 1)
    older_article = None
    if olders:
        older_article = olders[0]
    newer_article = None
    if newers:
        newer_article = newers[0]
    return (newer_article, older_article)

if __name__ == '__main__':
    # test add an article
    '''
    new_article = add_article(title="Where to learn programming?",
        description="Head to digolds.cn, it's a great place to share your idea!",
        markdown_content="# Hello Digolds!",
        created_date=get_time_stamp(12),
        author_name='digolds')
    articles[new_article['id']] = new_article
    new_article = add_article(title="Where to learn programming?",
        description="Head to digolds.cn, it's a great place to share your idea!",
        markdown_content="# Hello Digolds!",
        created_date=get_time_stamp(12 + 1),
        author_name='digolds')
    articles[new_article['id']] = new_article
    new_article = add_article(title="Where to learn programming?",
        description="Head to digolds.cn, it's a great place to share your idea!",
        markdown_content="# Hello Digolds!",
        created_date=get_time_stamp(12 + 2),
        author_name='digolds')
    articles[new_article['id']] = new_article
    '''

    # test sorted simple articles
    # sorted_simple_articles = list_simple_articles(True, get_time_stamp(0), 2)
    sorted_simple_articles = list_simple_articles(False, get_time_stamp(24 + 3), 2)
    print(sorted_simple_articles)
    assert(len(sorted_simple_articles) == 1)

    # test get an article
    new_article_copy = get_single_article(new_article['id'])
    assert(new_article_copy['CreatedDateTime'] == new_article['created_date'])
    
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
    assert(updated_article['Title'] == changed_title)

    # test delete an article
    #deleted_article = delete_article(new_article['id'])
    #assert(len(articles) == 4)