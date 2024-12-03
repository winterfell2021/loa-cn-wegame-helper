import requests
import re
import json
import datetime

def extract_packages(content):
    pattern = r'iPackageId:"(\d+)",sPackageId:"(\d+)",sImg:(.*?),sPackageName:"(.*?)"'
    matches = re.findall(pattern, content)
    packages = []
    for match in matches:
        iPackageId, sPackageId, _, sPackageName = match
        package = {
            "iPackageId": iPackageId,
            "sPackageId": sPackageId,
            "sPackageName": sPackageName
        }
        packages.append(package)

    return packages

def main():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    if month < 10:
        month = f"0{month}"
    url = f"https://mwegame.qq.com/helper/fz/score{str(year)[2:]}{month}/index.html"
    res = requests.get(url)
    html = res.text
    js_regex = re.compile(r'src=["\']([^"\']*index\.\w+\.js)["\']', re.IGNORECASE)
    matches = js_regex.findall(html)

    js_urls = []
    for src in matches:
        js_urls.append(src)
    url = js_urls[0]
    res = requests.get(url)
    flow_regex = re.compile(r'AMSRequest\.amsQueryByGameId\((\d+),(\d+),"fz"')
    matches = flow_regex.findall(res.text)
    activity_id = matches[0][0]
    flow_id = matches[0][1]
    exchange_regex = re.compile(r'AMSRequest\.amsActByGameId\((\d+),(\d+),"fz"')
    matches = exchange_regex.findall(res.text)
    exchange_flow_id = matches[0][1]
    packages = extract_packages(res.text)
    data = {
        "activity_id": activity_id,
        "flow_id": flow_id,
        "exchange_flow_id": exchange_flow_id,
        "packages": packages
    }
    with open(f"consts.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()