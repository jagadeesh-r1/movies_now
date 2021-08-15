#!/bin/bash

cd /home/ubuntu/movies_now  

git stash

git pull origin master

python3 serve.py



