#!/bin/bash
sudo apt-get install python3-pip nginx
sudo pip3 install -U pip
sudo pip3 install -U -r requirements.txt
sudo pip3 install -U gunicorn
sudo python3 setup_db.py

sudo /etc/init.d/nginx start

sudo rm /etc/nginx/sites-enabled/default
sudo rm /etc/nginx/sites-enabled/flask_project
sudo touch /etc/nginx/sites-available/flask_project
sudo ln -s /etc/nginx/sites-available/flask_project /etc/nginx/sites-enabled/flask_project
sudo bash -c 'echo "server {location / {proxy_pass http://localhost:8000; proxy_set_header Host \$host; proxy_set_header X-Real-IP \$remote_addr;}}" > /etc/nginx/sites-enabled/flask_project'

sudo /etc/init.d/nginx stop
