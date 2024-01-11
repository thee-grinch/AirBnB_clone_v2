#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

if ! command -v nginx > /dev/null; then
    sudo apt-get update
    sudo apt-get install nginx -y
fi
folders=("/data/" "/data/web_static/" "/data/web_static/releases/" "/data/web_static/releases" "/data/web_static/shared/" "/data/web_static/releases/test/")
for folder in "${folders[@]}"; do
    if [ ! -d "$folder" ]; then
        sudo mkdir -p "$folder"
    fi
done

#sudo touch "/data/web_static/releases/test/index.html"
echo "<h1>Hello from Testing</h1>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

printf %s "
server {
        listen 80 default_server;
        listen [::]:80 default_server;
        server_name priscacreations.tech;

        add_header X-Served-B $(hostname);
        root /var/www/html/;
        index index.html index.htm index.nginx-debian.html;

        location /hbnb_static {
            alias /data/web_static/current/;
            }
        location /redirect_me {
            return 301 http://google.com/;
        }
        error_page 404 /404.html;
        location /404 {
            root /var/www/html;
            internal;
        }
}" | sudo tee /etc/nginx/sites-available/default > /dev/null

sudo service nginx restart
