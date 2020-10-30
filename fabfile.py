#!/usr/bin/env python

__author__ = 'SLZ'

import os, re

from datetime import datetime
from fabric.api import *

from config import digolds_service_path, group, user, key_filename, ips, login_user

env.user = login_user
env.sudo_user = 'root'
env.hosts = ips
env.key_filename = key_filename

_TAR_FILE = 'dist-digolds.tar.gz'

_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE

_REMOTE_BASE_DIR = digolds_service_path

def _current_path():
    return os.path.abspath('.')

def _now():
    return datetime.now().strftime('%y-%m-%d_%H.%M.%S')

'''
fab zip
'''
def zip():
    includes = ['views','static', 'middlewares', 'controllers', 'favicon.ico', '*.py']
    excludes = ['test', '.*', '*.pyc', '*.pyo','__pycache__']
    local('rm -f %s' % _TAR_FILE)
    cmd = ['tar', '--dereference', '-czvf', '%s' % _TAR_FILE]
    cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
    cmd.extend(includes)
    local(' '.join(cmd))

'''
fab prepare
'''
def prepare():
    sudo('pip install gunicorn')
    sudo('pip install supervisor')
    sudo('yum -y install epel-release')
    sudo('yum -y install nginx')
    sudo(f'mkdir {_REMOTE_BASE_DIR}')
    sudo(f'groupadd {group}')
    sudo(f'adduser -g {group} {user}')

'''
fab deploy
'''
def deploy():
    newdir = 'www-%s' % _now()
    run('rm -f %s' % _REMOTE_TMP_TAR)
    put('%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)
    with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)
        run('python generate_configs.py')
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f www')
        sudo('ln -s %s www' % newdir)
        sudo('chown www-data:www-data www')
        sudo('chown -R www-data:www-data %s' % newdir)
    with settings(warn_only=True):
        run(f'supervisorctl -c {_REMOTE_BASE_DIR}/www/gunicorn.conf stop gunicorn')
        run(f'supervisorctl -c {_REMOTE_BASE_DIR}/www/gunicorn.conf start gunicorn')
        run('systemctl restart nginx')