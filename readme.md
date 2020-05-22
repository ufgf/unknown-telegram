# Unknown Telegram
## Requirements
* Python 3 (versions less than 3.7 were not tested)
* Git
* Hosting with a static file system (Heroku does not fit!)
* Understanding the actions performed

## Installation
```
$ sudo apt install -y git python3 python3-pip && git clone https://github.com/MaxUNof/unknown-telegram.git && cd unknown-telegram && sudo python3 -m pip install -r requirements.txt
```
## Starting
At the first start, the bot will ask for a phone number and code. This is necessary for the authorization procedure in Telegram.  
**Your data will sent only to the Telegram server.**
```
$ python3 main.py
```

Further, you can use a convenient way to launch a bot, for example: *screen, service, manually*.
