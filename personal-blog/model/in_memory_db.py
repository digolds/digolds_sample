import time
import copy

from model.articles_content import internet_content, internet_description, internet_title

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

def add_article(**kwargs):
    a = _generate_article(**kwargs)
    articles[a['id']] = a
    return a

def delete_article(id):
    a = articles.pop(id)
    return a

def get_single_article(id):
    return articles[id]

def update_single_article(**kwargs):
    title = kwargs.get("title")
    description = kwargs.get("description")
    markdown_content = kwargs.get("markdown_content")
    created_date = kwargs.get("created_date")
    author_name = kwargs.get("author_name")
    a = articles[kwargs.get("id")]
    a["title"] = title
    a["description"] = description
    a["markdown_content"] = markdown_content
    a["created_date"] = created_date
    a["author_name"] = author_name
    return a

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

_init_test_data()

if __name__ == '__main__':
    # test initialization
    _init_test_data()
    assert(len(articles) == 2)
    
    # test sorted detail articles
    sorted_articles = list_articles()
    assert(len(sorted_articles) == 2)
    assert(sorted_articles[0]["created_date"] > sorted_articles[1]["created_date"])
    
    # test sorted simple articles
    sorted_simple_articles = list_simple_articles()
    assert(len(sorted_simple_articles) == 2)
    assert(sorted_simple_articles[0]["created_date"] > sorted_simple_articles[1]["created_date"])
    assert('markdown_content' not in sorted_simple_articles)

    # test add an article
    new_article = add_article(title="Where to learn programming?",
        description="Head to digolds.cn, it's a great place to share your idea!",
        markdown_content="# Hello Digolds!",
        created_date=int(time.time()) + 2,
        author_name='digolds')
    assert(len(articles) == 3)

    # test get an article
    new_article_copy = get_single_article(new_article['id'])
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
    assert(updated_article['title'] == new_article['title'])

    # test delete an article
    deleted_article = delete_article(new_article['id'])
    assert(len(articles) == 2)