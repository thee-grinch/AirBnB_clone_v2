#!/usr/bin/env bash
#script to confingure nginx

if ! command -v nginx &> /dev/null; then
        apt update
        apt -y install nginx

fi
mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
#sudo touch /data/web_static/current/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
echo "Mordecai Muvandi" > /data/web_static/releases/test/index.html
chown -R ubuntu:ubuntu /data/

printf %s "
server {
        listen 80 default;
        listen [::]80 default;
        server_name muvandii.tech;
        add_header X-Served-By $HOSTNAME;
        root /var/www/html;
        index index.html index.htm;
        location /hbnb_static {
                alias /data/web_static/current/;
                index index.html, index.htm;
        }
        location /redirect_me {
                return 301 https://www.twitter.com/muvandii;
        }
        error_page 404 /404.html;
        location /404 {
                root /var/www/html;
                internal;
        }

}" > /etc/nginx/sites-available/default

service nginx start                     
