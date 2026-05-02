#! /usr/bin/env bash


if [ -f vars.sh ]; then
  source vars.sh
fi


# get organizaion name
while [[ ! $org =~ ^[a-z][a-z0-9_-]+$ ]]; do
  read -p "Enter an organization name: " org
done


# get instance name
while [[ ! $instance =~ ^[a-z][a-z0-9_-]+$ ]]; do
  read -p "Enter the instance name: " instance
done


# get workers count
while [[ ! $workers =~ ^[0-9]+$ ]]; do
  read -p "Enter the number of workers: " workers
done


# get domain
while [[ ! $domain =~ ^[a-z][a-z0-9\._]+$ ]]; do
  read -p "Enter the domain name: " domain
done


venv=/usr/local/lib/${org}/pyenv
py=${venv}/bin/python
pip=${venv}/bin/pip


# create virtual env
mkdir -p /usr/local/lib/${org}
python3 -m venv ${venv}


# install
${pip} install yhttp-markdown gunicorn


# systemd service
echo "\
[Unit]
Description=${org}/${instance} WSGI Application 
After=network.target
Wants=postgresql.service
After=postgresql.service

[Service]
# LimitNOFILE=4096:4096
Type=simple
RestartSec=2s
Restart=always
User=www-data
Group=www-data
WorkingDirectory=/etc/${org}
RuntimeDirectory=${org}
RuntimeDirectoryMode=0776
PIDFile=/run/${org}/${instance}.pid
ExecStart=${venv}/bin/gunicorn \
  --workers ${workers} \
  --bind unix:/run/${org}/${instance}.s \
  --pid /run/${org}/${instance}.pid \
  --chdir /etc/${org} \
  ${instance}wsgi:app

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/${instance}.service


# configuration
echo "\
title: HTTP Markdown Server
root: /var/wwww/agrin/apidoc
default: index.md

toc:
  depth: 3

# a list of regex patterns to exclude from TOC and HTTP serve
exclude:

metadata:
  physical: .ymdmetadata
  baseurl: /.ymdmetadata

highlight:
  theme: monokai
" > /etc/${org}/${instance}.yml


# wsgimodule
echo "\
import os
from yhttp.markdown.server import app


app.settings.loadfile('/etc/${org}/${instance}.yml')
app.ready()
" > /etc/${org}/${instance}wsgi.py


# TODO: nginx 
echo "\
upstream agrin.apidoc.upstream {
  server unix:/run/agrin/apidoc.s fail_timeout=1;
}

server {
  listen 80;
  server_name apidoc.agrn.ir;

  location / {
    proxy_set_header X-Forwarded-Host \$host;
    proxy_set_header X-Forwarded-Server \$host;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_pass http://agrin.apidoc.upstream;
  }
}
" > /etc/nginx/sites-available/${domain}
if [ -f /etc/nginx/sites-enabled/${domain} ]; then
  rm /etc/nginx/sites-enabled/${domain}
fi
ln -s /etc/nginx/sites-available/${domain} /etc/nginx/sites-enabled/ 


systemctl daemon-reload
systemctl enable ${instance}.service
systemctl restart ${instance}.service
systemctl status ${instance}.service --no-pager


echo "SUMMARY!"

echo Organization: ${org}
echo Instance: ${instance}
echo Workers: ${workers}
echo Virtual Environment: ${venv}
echo Systemd Unit: /etc/systemd/system/${instance}.service
