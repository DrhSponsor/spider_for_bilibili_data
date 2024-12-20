import requests
from bs4 import BeautifulSoup as bs

url = "https://tieba.baidu.com/f"
params = {
    "ie": "utf-8",
    "kw": "公务员",
    "fr": "search"
}
def get_tieba():
    r = requests.get(url,params=params)
    if r.status_code != 200:
        print('贴吧错误码',r.status_code)
        return '贴吧访问错误'
    num = bs(r.text, features='lxml').find(class_='card_infoNum').text
    # num是82,404 这样有逗号的
    num = int(num.replace(',',''))
    print('贴吧帖数',num)
    return num

if __name__ ==  '__main__':
    print(get_tieba())
