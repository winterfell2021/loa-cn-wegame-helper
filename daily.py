import requests
import time
import yaml
from loguru import logger
tasks = [
    {
        'iChartId': '351942',
        'iSubChartId': '351942',
        'sIdeToken': 'kwQGNV',
    },
     {
        'iChartId': '351951',
        'iSubChartId': '351951',
        'sIdeToken': '3DaEq5',
        'query': True,
    },
    {
        'iChartId': '353339',
        'iSubChartId': '353339',
        'sIdeToken': 'ktvhpC',
    },
    # {
    #     'iChartId': '353358',
    #     'iSubChartId': '353358',
    #     'sIdeToken': '1pSkEO',
    #     'typeId': 1,
    #     'nums': 1,
    # }
]
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
        for task in tasks:

            data = {
                # 'iChartId': '313865',
                # 'iSubChartId': '313865',
                # 'sIdeToken': 'FC0RcM',
                **task,
                'e_code': '0',
                'g_code': '0',
                'eas_url': 'http%3A%2F%2Flostark.qq.com%2Fcp%2Fa20241206newban%2F',
                'eas_refer': 'http%3A%2F%2Flostark.qq.com%2Fcp%2Fa20241206newban%2F%3Freqid%3De4c38e27-7bc7-411d-ac7f-6eb408181d3e%26version%3D27',
                'sMiloTag': 'AMS-fz-0811235523-NTeyaa-659629-1059453',
                'ams_targetappid': 'wx0a71413944e4c4d0',
                'channel': 'index',
            }

            response = requests.post('https://comm.ams.game.qq.com/ide/', cookies=cookies, headers=headers, data=data)
            print(response.json())
            time.sleep(2)