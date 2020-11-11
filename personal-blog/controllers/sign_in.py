#!/usr/bin/env python

__author__ = 'SLZ'

'''
sign-in controller.
'''
import hashlib
import time
import os

from digwebs.web import current_app, ctx

def make_signed_cookie(user_name, max_age):
    # build cookie string by: user_name-expires-md5
    expires = str(int(time.time() + max_age))
    L = [user_name, expires, hashlib.md5(f'{user_name}-{expires}'.encode('utf-8')).hexdigest()]
    return '-'.join(L)

def user_login_info():
    return (os.getenv('USER_NAME'), hashlib.md5(os.getenv('PASSWORD').encode('utf-8')).hexdigest())

@current_app.view('sign-in.html')
@current_app.get('/views/sign-in')
def sign_in():
    return dict()

@current_app.api
@current_app.post('/api/v1/sign-in')
def api_sign_in():
    i = ctx.request.input()
    user_name = i.user_name.strip()
    md5_password = i.md5_password.strip()
    login_info = user_login_info()
    passed = login_info[0] == user_name and login_info[1] == md5_password
    if passed:
        max_age = 24 * 60 * 60 # one day
        cookie = make_signed_cookie(user_name, max_age)
        ctx.response.set_cookie('admin', cookie, max_age=max_age)
    return dict(passed = passed)