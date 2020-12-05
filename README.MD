# PickPic

PickPic is a social network build for one simple reason - saving images in cloud by using one script (written in JS and looks like a bookmark). If you don't want to save all images to your local disk you can simply do it using PickPic. This project build with Django/Python, Redis, JQuery/JS, SQL.

## Installation

Simply clone the repo and install requirements
```
pip install -r requirements.txt
```
Also don't forget to install and run Redis-server (it is important for fast counting likes).

## Usage

Application configured to work with Redis through standard port number, so firstly you need to run redis-server:
```
src/redis-server
```
and then run the django application server:
```
python manage.py runserver
```

## Features
