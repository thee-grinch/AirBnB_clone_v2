#!/usr/bin/env bash
#script to confingure nginx

if !command -v nginx &> /dev/null; then
        sudo apt update
        sudo apt -y install nginx

fi
sudo mkdir -p /data/ /data/web_static/ /data/web_static/releases/test/ /data/web_static/shared/
#sudo touch /data/web_static/current/index.html
echo "Mordecai Muvandi" | sudo tee /data/web_static/current/index.html > /dev/null
sudo chown -R ubuntu:ubuntu /data/
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
printf %s "
server {
        listen 80 default;
        listen [::]80 default;
        server_name muvandii.tech;
        location /hbnb_static {
                alias /data/web_static/current/;
        }
}" | sudo tee /etc/nginx/site-enabled/default > /dev/null

sudo service nginx start                     
