#!/bin/bash
echo "Configuring nginx..."
scriptdir=$(realpath $(dirname $0))
basedir=$(realpath $(dirname $scriptdir))
# Install custom service definition
cp $scriptdir/nginx/nginx.service /lib/systemd/system/nginx.service

# Install site config
nginxconf=$(<$scriptdir/nginx/wagtail.nginx.template)
echo "${nginxconf//<REPLACEME>/$basedir}" > /etc/nginx/sites-enabled/wagtail.nginx
# cat /etc/nginx/sites-enabled/wagtail.nginx

# Update service
systemctl enable nginx
systemctl restart nginx
systemctl status nginx