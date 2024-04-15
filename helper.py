import time
import requests
import logging
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)
HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}
BASE_URL = "https://api2.helper.qq.com"


class User:
    def __init__(self, app_id: str, access_token: str, open_id: str):
        self.app_id = app_id
        self.access_token = access_token
        self.open_id = open_id
        self.userId = 0
        self.roleId = 0
        self.xy_role_id = 0
        self.momentId = 260841843
        self.token = ""
        self.message = ""

    def _check_response(self, res):
        if res.status_code != 200:
            raise Exception(f"Failed to request: {res.text}")
        data = res.json()
        if data["result"] != 0:
            raise Exception(f"Failed to request: {data}")
        return data

    def login(self):
        url = f"{BASE_URL}/user/login"
        payload = f"cSystemVersionName=7.1.2&cClientVersionCode=2103070023&loginType=qqConnect&nickname=%&keyType=0&lastGetRemarkTime=0&openid={self.open_id}&autoLogin=0&cGameId=1010&accessToken={self.access_token}&cCurrentGameId=1010&cSystem=android&expiresIn=7776000"
        res = requests.post(url, headers=HEADERS, data=payload)
        try:
            data = self._check_response(res)
            self.userId = data["data"]["userId"]
            self.token = data["data"]["token"]
            self.uin = data["data"]["uin"]
            self.message += f"用户ID：{self.userId}\n"
        except Exception as e:
            raise e

    def enhance_payload(self, payload: str = ""):
        return (
            f"gameId=10040&userId={self.userId}&token={self.token}&cGameId=1010&cCurrentGameId=10040&"
            + payload
        )

    def get_main_role(self):
        url = f"{BASE_URL}/game/chatroles"
        payload = self.enhance_payload()
        res = requests.post(url, headers=HEADERS, data=payload)
        try:
            data = self._check_response(res)
            self.roleId = data["data"]["roles"][0]["roleId"]
            logger.info(f"Main role: {self.roleId}")
        except Exception as e:
            raise e

    def view_role_detail(self):
        url = f"{BASE_URL}/play/lostarkroledetail"
        payload = self.enhance_payload(f"roleId={self.roleId}")
        res = requests.post(url, headers=HEADERS, data=payload)
        try:
            data = self._check_response(res)
            logger.debug(f"Role detail: {data}")
        except Exception as e:
            raise e

    def add_comment(self, moment_id: int):
        url = f"{BASE_URL}/moment/addcomment"
        payload = f"content=&gameIds=&syncFriendFeed=1&roleId={self.roleId}&cChannelId=1&secret=2&qaLabels=%5B%5D&forwardId=0&type=1&momentId={moment_id}&cleIds=%5B%5D&cGameId=1010&links=%5B%5D&cCurrentGameId=10040&text=1&labels="
        payload = self.enhance_payload(payload)
        res = requests.post(url, headers=HEADERS, data=payload)
        try:
            data = self._check_response(res)
            logger.info(f"Comment added: {data['data']}")
        except Exception as e:
            raise e

    def view_moment_detial(self, moment_id: int):
        url = f"{BASE_URL}/moment/detail"
        payload = f"momentId={moment_id}"
        payload = self.enhance_payload(payload)
        res = requests.post(url, headers=HEADERS, data=payload)
        try:
            data = self._check_response(res)
            logger.info(f"Moment detail: {data['data']}")
        except Exception as e:
            raise e

    def view_shop(self):
        url = f"{BASE_URL}/user/event"
        payload = self.enhance_payload("buttonId=34096")
        res = requests.post(url, headers=HEADERS, data=payload)
        try:
            data = self._check_response(res)
            logger.info(f"Shop: {data['data']}")
        except Exception as e:
            raise e

    def like_moment(self, moment_id: int, like: int = 1):
        url = f"{BASE_URL}/moment/like"
        payload = f"momentId={moment_id}&type={like}"
        payload = self.enhance_payload(payload)
        res = requests.post(url, headers=HEADERS, data=payload)
        try:
            data = self._check_response(res)
            logger.info(f"Comment liked: {data['data']}")
        except Exception as e:
            raise e

    def add_moment(self):
        url = f"{BASE_URL}/moment/add"
        payload = f"content=&gameIds=&syncFriendFeed=1&roleId={self.roleId}&cChannelId=1&secret=2&qaLabels=%5B%5D&forwardId=0&type=1&momentId=0&cleIds=%5B%5D&cGameId=1010&links=%5B%5D&cUin=&text=1&labels="
        payload = self.enhance_payload(payload)
        res = requests.post(url, headers=HEADERS, data=payload)
        try:
            data = self._check_response(res)
            self.momentId = data["data"]["momentId"]
            logger.info(f"Comment added: {data['data']}")
        except Exception as e:
            raise e

    def list_info(self):
        url = f"{BASE_URL}/game/listinfov2"
        payload = self.enhance_payload(
            "chanType=text&pos2=1&cChannelId=1&parentType=27011200&type=27011199&page=1&pos1=1"
        )
        res = requests.post(url, headers=HEADERS, data=payload)
        try:
            data = self._check_response(res)
            i = 0
            for info in data["data"]["list"]:
                info_id = info["iInfoId"]
                logger.info(f"查看资讯，info_id = {info_id}")
                i += 1
                self.update_info_view(info_id)
                time.sleep(2)
                if i == 2:
                    break
        except Exception as e:
            raise e

    def update_info_view(self, info_id: int):
        url = f"{BASE_URL}/game/detailinfov2"
        payload = self.enhance_payload(f"iInfoId={info_id}&pos=3&apiVersion=1")
        res = requests.post(url, headers=HEADERS, data=payload)
        try:
            data = self._check_response(res)
            # print(data)
            logger.info(f"资讯查看成功")
        except Exception as e:
            raise e

    def get_task_info(self):
        url = f"https://mwegame.qq.com/fe/s/la/task?areaId=50&userId={self.userId}&cGameId=1010&gameId=10040&token={self.token}&appid={self.app_id}&appOpenid={self.open_id}&accessToken={self.access_token}&uniqueRoleId={self.roleId}&accType=qc"

        headers = {
            "Host": "mwegame.qq.com",
            "Cookie": f"accessToken={self.access_token}; access_token={self.access_token}; acctype=qc; appId={self.app_id}; appOpenId={self.open_id}; appOpenid={self.open_id}; appid={self.app_id}; openId={self.open_id}; openid={self.open_id};",
            "gh-header": "2-2-1010-2103070017-757116932",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 GH_QQConnect GameHelper_1010/1.1.0.17.2103070017",
        }
        response = requests.request("GET", url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        axis_line_items = soup.select(".axis-line-item")
        for item in axis_line_items:
            title = item.find("h5", class_="title").text.strip()
            desc = item.find("p", class_="desc").text.strip()
            complete = item.find("button", class_="btn").text.strip() == "已完成"
            if not complete:
                if title == "每日参与资讯/动态评论3次":
                    for i in range(3):
                        self.add_comment(self.momentId)
                        time.sleep(5)
                elif title == "每日发布动态":
                    self.add_moment()
                elif title == "每日浏览动态详情3则":
                    for i in range(3):

                        self.view_moment_detial(self.momentId - i)
                        time.sleep(5)

                elif title == "每日访问APP商城":
                    self.view_shop()
                elif title == "每日查看角色卡详情页":
                    self.view_role_detail()
                elif title == "每日在资讯/动态点赞5次":
                    for i in range(5):
                        self.like_moment(self.momentId + 5 + i, 1)
                        time.sleep(2)
                        self.like_moment(self.momentId + 5 + i, 0)
                        time.sleep(5)
                elif title == "每日浏览文章资讯2篇":
                    self.list_info()
            self.message += f"【{title}】{'已完成' if complete else '未完成'}\n"
            logging.info(f"{title} - {desc} - {complete}")

    def get_score(self):
        url = "https://act.game.qq.com/ams/ame/amesvr?ameVersion=0.3&sServiceType=fz&iActivityId=629910&sServiceDepartment=xinyue&sSDID=&sMiloTag=f&_="
        payload = f"userId={self.userId}&userToken={self.token}&uin={self.uin}&sServiceType=fz&uGid=251&iActivityId=629910&iFlowId=1025934&g_tk=1842395457&e_code=0&g_code=0&eas_url=http%3A%2F%2Fmwegame.qq.com%2Fhelper%2Ffz%2Fscore%2F&eas_refer=http%3A%2F%2Fact.xinyue.qq.com%2F%3Freqid%3D%26version%3D27&sServiceDepartment=xinyue"
        headers = {
            "Host": "act.game.qq.com",
            "Cookie": f"access_token={self.access_token}; acctype=qc; appid={self.app_id}; openid={self.open_id};",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 GH_QQConnect GameHelper_1010/1.1.0.17.2103070017",
        }
        res = requests.post(url, data=payload, headers=headers).json()
        score = res["modRet"]["sOutValue1"]
        jyp, yb = res["modRet"]["sOutValue2"].split(",")[:2]
        logger.info(f"当前积分：{score}，交易牌={jyp}，银币={yb}")
        self.message += f"当前积分：{score}，交易牌={jyp}，银币={yb}\n"
        self.get_xy_role()
        if jyp == "1":
            self.exchange(3185172)
            time.sleep(5)
        if yb == "1":
            self.exchange(3185174)

    def get_xy_role(self):
        url = "https://agw.xinyue.qq.com/amp2.RoleSrv/GetSpecifyRoleList"

        payload = {"game_code": "fz", "partition_id": 500005, "device": "others"}
        headers = {
            "Host": "agw.xinyue.qq.com",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "T-APPID": str(self.app_id),
            "T-ACCOUNT-TYPE": "qc",
            "Sec-Fetch-Site": "same-site",
            "T-ACCESS-TOKEN": self.access_token,
            "T-MODE": "true",
            "T-OPENID": self.open_id,
            "Sec-Fetch-Mode": "cors",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Origin": "https://mwegame.qq.com",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 GH_QQConnect GameHelper_1010/1.1.0.17.2103070017",
            "Referer": "https://mwegame.qq.com/",
            "Sec-Fetch-Dest": "empty",
        }

        res = requests.request("POST", url, headers=headers, json=payload).json()
        self.xy_role_id = res["roles"][0]["role_id"]
        logger.info(f"心悦角色ID：{self.xy_role_id}")

    def exchange(self, exchange_id):
        url = f"https://act.game.qq.com/ams/ame/amesvr?ameVersion=0.3&sServiceType=fz&iActivityId=629910&sServiceDepartment=xinyue&sSDID=&sMiloTag=f&_="
        payload = f"gameId=&sArea=50&iSex=&sRoleId={self.xy_role_id}&iGender=&uGid=251&sPlatId=2&sPartition=5&sServiceType=fz&actQuantity=1&exchangeNo={exchange_id}&uin={self.uin}&userId={self.userId}&userToken={self.token}&cGameId=1010&subGameId=10040&objCustomMsg=&areaname=&roleid=&rolelevel=&rolename=&areaid=&iActivityId=629910&iFlowId=1025931&g_tk=1842395457&e_code=0&g_code=0&eas_url=http%3A%2F%2Fmwegame.qq.com%2Fhelper%2Ffz%2Fscore%2F&eas_refer=http%3A%2F%2Fact.xinyue.qq.com%2F%3Freqid%3D09%26version%3D27&sServiceDepartment=xinyue"
        headers = {
            "Host": "act.game.qq.com",
            "Cookie": f"access_token={self.access_token}; acctype=qc; appid={self.app_id}; openid={self.open_id};",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 GH_QQConnect GameHelper_1010/1.1.0.17.2103070017",
        }
        res = requests.post(url, data=payload, headers=headers).json()
        print(res)
