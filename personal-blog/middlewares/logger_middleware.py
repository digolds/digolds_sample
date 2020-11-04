import logging
import hashlib
import time

from digwebs.errors import seeother


def parse_signed_cookie(cookie_str):
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        user_name, expires, md5 = L
        if int(expires) < time.time():
            return None
        if user_name != "slz":
            return None
        if md5 != hashlib.md5(f'{user_name}-{expires}'.encode('utf-8')).hexdigest():
            return None
        return user_name
    except:
        return None

def log_record(ctx, next):
    user_name = None
    cookie = ctx.request.cookies.get('admin')
    if cookie:
        user_name = parse_signed_cookie(cookie)
    
    ctx.request.user_name = user_name
    if not user_name and ctx.request.path_info.startswith('/manage/'):
        raise seeother('/')
    
    if user_name and ctx.request.path_info == '/views/sign-in':
        raise seeother('/')
    return next()

def logger_middleware():
    return (log_record, 0)