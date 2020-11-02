import logging
from digwebs.errors import seeother

def log_record(ctx, next):
    if ctx.request.path_info.startswith('/manage/'):
        raise seeother('/')
    return next()

def logger_middleware():
    return (log_record, 0)