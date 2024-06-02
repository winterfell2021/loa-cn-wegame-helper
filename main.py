import logging

import yaml
from helper import User
from send_notify import send
import time
import traceback

logging.basicConfig(level=logging.INFO)
APP_ID = 102037747

if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    for user in config["users"]:
        try:
            user = User(APP_ID, user["access_token"], user["open_id"])
            user.login()
            user.get_main_role()
            user.get_task_info()
            user.get_score()
            if user.notify:
                send('掌上命运方舟积分活动', user.message)
        except Exception as e:
            traceback.print_exc()
            print(f"Error: {e}")
        time.sleep(5)