import json
import requests

url = "https://tiku.fenbi.com/api/xingce/jammy/enroll/list"

def get_fenbi_token():
    with open('./fenbiToken.txt', "r", encoding="utf-8") as file:
        data = file.read().split('\n')
        userID = data[0]
        if userID is None:
            return 'Cannot get token'
        sess = data[1]
        return userID,sess

def get_fenbi():
    userID,sess = get_fenbi_token()
    cookies = {'userid':str(userID),
               'sess':str(sess)}
    r = requests.get(url,cookies=cookies)
    if r.status_code != 200:
        return '粉笔访问错误'
    data = json.loads(r.text)
    return int(data["data"]["enrollList"][0]["enrollNumber"])