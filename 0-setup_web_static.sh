#!/usr/bin/env bash
#script to confingure nginx

if !command -v nginx &> /dev/null; then
        sudo apt update
        sudo apt -y install nginx

fi
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
#sudo touch /data/web_static/current/index.html
sudo chown -R ubuntu:ubuntu /data/
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
echo "Mordecai Muvandi" | sudo tee /data/web_static/current/index.html > /dev/null

printf %s "
server {
        listen 80 default;
        listen [::]80 default;
        server_name muvandii.tech;
        add_header X-served-BY $HOSTNAME;
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

}" | sudo tee /etc/nginx/sites-available/default > /dev/null

sudo service nginx start                     
