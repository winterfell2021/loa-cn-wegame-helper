# lostark wegame helper

## Setup
- copy config.yaml.example to config.yaml
- fill cookie in config.yaml
- run with tg notify:
```
export TG_PROXY_HOST="localhost"
export TG_PROXY_PORT='7890'
export TG_BOT_TOKEN=''
export TG_USER_ID=''
python3 main.py
```

## How to Obtain Your Cookie
- Open the Charles proxy application.
- Start the app that requires monitoring.
- Search for requests directed to the host `appsupport.qq.com`.
- Locate the Cookie field in one of these requests; this is the value you need.
Note: The cookie typically expires in about 3 months.

## Notify
See in [qinglong](https://github.com/whyour/qinglong/blob/develop/sample/notify.py)