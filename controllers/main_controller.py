#!/usr/bin/env python

__author__ = 'SLZ'

'''
digwebs framework controller.
'''

from digwebs.web import current_app

@current_app.get('/')
def hello_world():
    return """
<html>
    <style>
    html,body{
  height:100%;
  padding:0;
  margin:0;
}
*{
  box-sizing:border-box;
}

.container{
  
  width:100%;
  height:100%;
  
  display:flex;
  justify-content:center;
  align-items:center;
  
}
    </style>
    <body>
    <div class="container">
  <h1>digwebs - A Minimal Web Framework!</h1>
</div>
    </body></html>
"""

in_memory_blogs = []

@current_app.get('/blogs')
def blogs():
  global in_memory_blogs
  res = ""
  for b in in_memory_blogs:
    res += f"<li>{b}</li>"
  
  return f"""
    <html>
        <h1>My Blogs</h1>
        <ul>
            {res}
        </ul>
    </html>
    """

@current_app.post('/blog/:blog_title')
def add_blog(blog_title):
  global in_memory_blogs 
  if blog_title not in in_memory_blogs:
    in_memory_blogs.append(blog_title)
  return f"""
    <html>
        <h1>Create Blog</h1>
        <span>{blog_title}</span>
    </html>
  """

@current_app.delete('/blog/:blog_title')
def delete_blog(blog_title):
  global in_memory_blogs 
  if blog_title in in_memory_blogs:
    in_memory_blogs.remove(blog_title)
  return f"""
    <html>
        <h1>Blog to be deleted</h1>
        <span>{blog_title}</span>
    </html>
  """

@current_app.put('/blog/:blog_title/:new_title')
def update_blog(blog_title, new_title):
  global in_memory_blogs 
  if blog_title in in_memory_blogs:
    in_memory_blogs[in_memory_blogs.index(blog_title)] = new_title
  return f"""
    <html>
        <h1>Blog to be modified</h1>
        <p>Old title: {blog_title}</p>
        <p>New title: {new_title}</p>
    </html>
  """