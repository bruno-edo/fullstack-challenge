#!/bin/bash
sudo /etc/init.d/nginx start
sudo gunicorn -w 4 -b localhost:8000 main:app
