##Synonysms Dictuinary
- Synonysms Dictuinary is simple dictionary BOT return "definitions and synonyms" in separated message bubble
- Run on: python
- Deploy on: Heroku https://www.heroku.com
- Connect to: https://developers.line.me
- Using: LINE message api BOT: https://developers.line.me/en/docs/messaging-api/building-bot/
- Using: LINE replyToken https://developers.line.me/en/docs/messaging-api/reference/#send-reply-message.
- Using: Use dictionary API from https://developer.oxforddictionaries.com
- Git: https://github.com/iamgique/line-synonyms-dictionary.git

####You can add LINE bot Synonysms Dictuinary at QR Code below:
![alt text](https://qr-official.line.me/M/xEjdR8Vlu0.png)

## Prerequisite
Make sure you have [python](https://www.python.org) and the [pip](https://pip.pypa.io/en/stable/installing/) installed.

##Prepare
Flask==1.0.2
gunicorn==19.8.1
itsdangerous==0.24
Jinja2==2.10
MarkupSafe==1.0
requests==2.11.1
six==1.4.1
urllib3==1.22
Werkzeug==0.14.1

## Deploying to Heroku
```
$ heroku create
$ git push heroku master
$ heroku open
```

## Change source code
```
$ heroku git:remote -a {heroku app name}
$ git add .
$ git commit -m "First commit"
$ git push heroku master
```

## Logs
```
$ heroku logs --tail
```

## Run on local
```
$ python app.py
```