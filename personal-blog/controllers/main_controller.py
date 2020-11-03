#!/usr/bin/env python

__author__ = 'SLZ'

'''
digwebs framework controller.
'''

from digwebs.web import current_app

@current_app.view('home.html')
@current_app.get('/')
def home_page():
    return dict(name="slz")