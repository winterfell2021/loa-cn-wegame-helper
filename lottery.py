import requests
import time
import yaml
from loguru import logger
TASK_MAPPING = {
    'sEncrypt': {
        'iChartId': '361015',
        'iSubChartId': '361015',
        'sIdeToken': 'rZPTAH',
    },
    'normal': {
        'iChartId': '362060',
        'iSubChartId': '362060',
        'sIdeToken': 'IXeiQA',
        'type': 1,
    },
    'receive': {
        'iChartId': '364250',
        'iSubChartId': '364250',
        'sIdeToken': 'zDkeHT',
        'type': 2,
    }
}

def do_task(user, task):
    cookies = {
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
    return response.json()

if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    for i in range(0, len(config["users"]), 4):
        users = config["users"][i:i+4]
        logger.info(f"users: {len(users)} for batch {i//4+1}")
        s_encrypt_list = []
        for user in users:
            s_encrypt = do_task(user, TASK_MAPPING['sEncrypt'])['jData']['sEncrypt']
            s_encrypt_list.append(s_encrypt)
            receive_resp = do_task(user, TASK_MAPPING['receive'])
            print(receive_resp)
            time.sleep(1)
        for i, user in enumerate(users):
            for j, s_encrypt in enumerate(s_encrypt_list):
                if i == j:
                    continue
                print(f"user: {i+1}, 去助力 s_encrypt: {j+1}")
                task = TASK_MAPPING['normal']
                task['sEncrypt'] = s_encrypt
                task['type'] = 1
                resp = do_task(user, task)
                print(resp)
                time.sleep(2)
