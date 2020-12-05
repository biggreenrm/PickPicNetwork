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

Firstly, to start using this service, user has to register and login. Here is the registration page:

![Alt text](https://github.com/biggreenrm/PickPicNetwork/blob/master/readme_screenshots/registration.png)


After proceeding registration, user will come to main page, also called Dashboard. There is proposal to drag "bookmark it button" to user's bookmark toolbar. This is how it works.

![Alt text](https://github.com/biggreenrm/PickPicNetwork/blob/master/readme_screenshots/dashboard.png)


After user adds this button to bookmarks, he will have th ability to click it on any page and see all images he can saves to his account. After that, all user's saved images will be stored in 'Images' page.

![Alt text](https://github.com/biggreenrm/PickPicNetwork/blob/master/readme_screenshots/bookmarked_images.png)


There also opportunity to follow other users and see what they add to their page. This fills user's feed. To see who also are registered in project you should click on 'People' button (and I'm terribly sorry for my sense of humor):

![Alt text](https://github.com/biggreenrm/PickPicNetwork/blob/master/readme_screenshots/users_list.png)


User also has opportunity to visit image's page (no matter his or another), and 'like' it. There is also view counter. And bad humor again:

![Alt text](https://github.com/biggreenrm/PickPicNetwork/blob/master/readme_screenshots/image_page.png)

So, that's it. I tried to be short.

## Tech-stack
Python, Django, Redis, JS, JQuery, SQL, HTML/CSS

## Project status
Work stopped