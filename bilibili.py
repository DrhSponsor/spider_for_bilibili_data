import json
import random
import re
import time

import requests,ast
from bs4 import BeautifulSoup
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://www.bilibili.com/",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}
cookies = {
    "buvid3": "4E8B454A-4F41-D671-B4A4-3515F44A2A1222848infoc",
    "b_nut": "1731575921",
    "buvid4": "F979D682-785D-57D6-D57B-4670D187C9E922848-024111409-BBqjy+iBHoQvVgTiqud3wg%3D%3D",
    "b_lsid": "7C710AFDD_19329F7BC83",
    "_uuid": "36E81099B-DE4F-3ADE-386E-6A968C3CF1010E21798infoc",
    "buvid_fp": "37959052a5736f00ad55c65ba9b4ce2b"
}
url = 'https://search.bilibili.com/all'
params = {
    "keyword": "公考",
    "from_source": "webtop_search",
    "spm_id_from": "333.1007",
    "search_source": "5"
}

basic_bv_url = 'https://www.bilibili.com/video/'

bv_list = []

def getBV():
    # 读取 BV.txt
    with open('./BV.txt', "r", encoding="utf-8") as file:
        content = file.read().strip()

    # 安全解析 BV 号列表
    try:
        # 有bv列表的话
        bv_list = ast.literal_eval(content)
        print("解析的 BV 号数组：", bv_list)
    except Exception as e:
        bv_list = list(set(get_BV_by_keyword('公考')+get_BV_by_keyword('行测')+get_BV_by_keyword('申论')))
    return bv_list


def get_BV_by_keyword(keyword):
    bv_list = []
    page = 1
    while page < 21:
        print('looping')
        params['keyword'] = keyword
        params['page'] = page
        r = requests.get(url,headers=headers,cookies=cookies,params=params)
        if r.status_code != 200:
            return 'Network fail'
        bs = BeautifulSoup(r.text,features='lxml')
        href_list = bs.find_all('a',href=re.compile(r"^//www\.bilibili\.com/video/"))
        # print('href_list',href_list)
        for href in href_list:
            href = href['href']
            if 'video' in href:
                bv = href.split('/')[-2]
                if bv not in bv_list:
                    bv_list.append(bv)
                    print(bv)
        page += 1
        time.sleep(random.uniform(0.5, 1.5))
    return bv_list

def get_all_by_bv(bv):
    r = requests.get(basic_bv_url+bv+'/',headers=headers,cookies=cookies)
    bs = BeautifulSoup(r.text,features='lxml')

    fans = get_fans(bs)
    if fans is False:
        return '创作团队'

    stat = bs.find('script', text=re.compile(r'"stat":\s*{'))
    json_text = re.search(r'"stat":\s*({.*?})', stat.string)
    stat_data = json.loads(json_text.group(1))
    try:
        return {
            'view':stat_data['view'],
            'like':stat_data['like'],
            'share':stat_data['share'],
            'coin':stat_data['coin'],
            'reply':stat_data['reply'],
            'danmaku':stat_data['danmaku'],
            'favorite':stat_data['favorite'],
            'fans':get_fans(bs),
        }
    except Exception as e:
        return {'bv':bv,'error':e}
def deal_wan(text):
    if text[-1] == '万':
        # 比如1.9万
        return int(float(text.split('万')[0]) * 10000)
    else:
        return int(text)

# def get_view(bs):
#     view = bs.find(class_='view-text').text
#     return deal_wan(view)
# def get_like(bs):
#     like = bs.find(class_='video-like-info').text
#     return deal_wan(like)
# def get_share(bs):
#     share = bs.find(class_='video-share-info').text
#     return deal_wan(share)
# def get_coin(bs):
#     coin = bs.find(class_='video-coin-info').text
#     return deal_wan(coin)
# def get_comment(bs):
#     print('comment')
#     comment = bs.find('div',id='count').text.strip('"')
#     return deal_wan(comment)
# def get_bullet(bs):
#     print('bullet')
#     bullet = bs.find(class_='dm-text').text
#     return deal_wan(bullet)
# def get_collection(bs):
#     print('collection')
#     collection = bs.find(class_='video-fav-info').text
#     return deal_wan(collection)
def get_fans(bs):
    try:
        fans = bs.find(class_='follow-btn-inner').text.strip('"').strip().split(' ')[1]
    except Exception:
        return False
    return deal_wan(fans)
# def get_duration(bs):
#     print('duration')
#     # 秒数有可能是1:10:29 或者 20:30 不同位数
#     duration = bs.find(class_='bpx-player-ctrl-time-duration').text
#     if len(duration) == 2:
#         return duration[0] * 60 + duration[1]
#     else:
#         return duration[0] * 3600 + duration[1] * 60 + duration[2]

if __name__ == '__main__':
    getBV()