#!/bin/bash
pip install gunicorn
pip install supervisor
yum -y install epel-release
yum -y install nginx
mkdir /srv/digolds
groupadd www-data
adduser -g www-data www-data

curl -o /tmp/p.tar.gz https://github.com/digolds/digolds_sample/archive/v0.0.1.tar.gz
tar xf /tmp/original.tar.gz -C /srv/digolds