import json
import requests

url = "https://tiku.fenbi.com/api/xingce/jammy/enroll/list"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "origin": "https://fenbi.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://fenbi.com/",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}
cookies = {
    "persistent": "HspmWFKIbVitVrwZFk76/IGRFJbWVuKTURo1xL3fhlvXodz4Nzuq3IDl8yMVwQf9mCzb8++AJKgGwrlYYWIpGw==",
    "_ga": "GA1.2.967441941.1732031561",
    "_gid": "GA1.2.945923755.1732031561",
    "_ga_Z92YWZPKSM": "GS1.2.1732031562.1.0.1732031562.0.0.0",
    "Hm_lvt_e7351028cde0d0ccb9ccdbe5fe531683": "1731413797,1731759452,1731907709,1732031570",
    "HMACCOUNT": "16E81E86DF76ABEE",
    "acw_tc": "0bd17c6217320315791477885e0a0ea0b2eeed5319aa4e6dc39232a8b675a5",
    "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%22141476644%22%2C%22first_id%22%3A%221932058096f119e-0f240795ceb24-26001f51-2073600-193205809701265%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Ffenbi.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzMjA1ODA5NmYxMTllLTBmMjQwNzk1Y2ViMjQtMjYwMDFmNTEtMjA3MzYwMC0xOTMyMDU4MDk3MDEyNjUiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxNDE0NzY2NDQifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22141476644%22%7D%2C%22%24device_id%22%3A%221932058096f119e-0f240795ceb24-26001f51-2073600-193205809701265%22%7D",
    "Hm_lpvt_e7351028cde0d0ccb9ccdbe5fe531683": "1732033178",
    "userid": "141476644"
}
params = {
    "app": "web",
    "av": "100",
    "hav": "100",
    "kav": "100",
    "client_context_id": "dc5b356efd7efc8361d7c163b586c71d"
}

def get_fenbi_token():
    with open('./fenbiToken.txt', "r", encoding="utf-8") as file:
        data = file.read().split('\n')
        userID = data[0]
        if userID is None:
            return 'Cannot get token'
        sess = data[1]
        return userID,sess

def get_fenbi():
    # userID,sess = get_fenbi_token()
    # cookies = {'userid':str(userID),
    #            'sess':str(sess)}
    r = requests.get(url,headers=headers,params=params,cookies=cookies)
    if r.status_code != 200:
        print("粉笔状态码",r.status_code)
        print('粉笔访问错误')
        return '粉笔访问错误'
    data = json.loads(r.text)
    enrollCount = int(data["data"]["enrollList"][0]["enrollNumber"])
    print('粉笔人数',enrollCount)
    return enrollCount
