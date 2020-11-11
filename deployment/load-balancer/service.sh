#!/bin/bash
pip install gunicorn
pip install supervisor
yum -y install epel-release
yum -y install nginx
mkdir /srv/digolds
groupadd www-data
adduser -g www-data www-data