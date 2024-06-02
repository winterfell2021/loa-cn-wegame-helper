import requests
import time
import yaml
from loguru import logger

if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    users = config["users"]
    logger.info(f"users: {len(users)}")

    for user in users:
        cookies = {
            # 'pgv_pvid': '7650512750',
            'acctype': 'qc',
            'openid': user['open_id'],
            'access_token': user['access_token'],
            'appid': '102037747',
        }

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'dnt': '1',
            'origin': 'https://lostark.qq.com',
            'referer': 'https://lostark.qq.com/',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        data = {
            'iChartId': '289989',
            'iSubChartId': '289989',
            'sIdeToken': 'FC0RcM',
            'e_code': '0',
            'g_code': '0',
            'eas_url': 'http%3A%2F%2Flostark.qq.com%2Fcp%2Fa20240516exstore%2F',
            'eas_refer': 'http%3A%2F%2Flostark.qq.com%2Fcp%2Fa20240516exstore%2F%3Freqid%3D3dff389c-9cca-4eeb-80a6-728de62064f6%26version%3D27',
            'sMiloTag': 'AMS-fz-0523204125-4LSI0C-640300-1037162',
            'ams_targetappid': 'wx0a71413944e4c4d0',
            'channel': 'index',
        }

        response = requests.post('https://comm.ams.game.qq.com/ide/', cookies=cookies, headers=headers, data=data)
        print(response.json())
        time.sleep(2)