#!/bin/sh
scriptdir=$(dirname $0)
# Install custom service definition
cp $scriptdir/nginx/nginx.service /lib/systemd/system/nginx.service

# Install site config
nginxconf=$(<$scriptdir/nginx/wagtail.nginx.template)
echo "${nginxconf//<REPLACEME>/$scriptdir}" > /etc/nginx/sites-enabled/wagtail.nginx
# cat /etc/nginx/sites-enabled/wagtail.nginx

# Update service
systemctl enable nginx
systemctl start nginx
systemctl status nginx
