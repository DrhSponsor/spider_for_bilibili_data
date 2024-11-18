from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests

# 事业编报名页面的 URL
url = "https://www.shiyebian.net/baoming.html"

def get_shiyebian():
    try:
        # 发送请求
        r = requests.get(url)
        # 检查请求状态
        if r.status_code != 200:
            print('事业编错误码',r.status_code)
            return '事业编访问错误'
        # 设置编码为 GBK
        r.encoding = 'gbk'
        soup = BeautifulSoup(r.content, "html.parser")

        # 获取昨天的日期，格式为 "2024年11月25日"
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y年%m月%d日")

        # 查找所有的日期行
        date_rows = soup.find_all("tr", class_="box-head")

        # 初始化统计数量
        count = 0

        # 遍历所有日期行，查找昨天的报名信息
        for date_row in date_rows:
            date_text = date_row.text

            # 检查是否为昨天的日期
            if yesterday in date_text:
                # 统计后面的地区行
                next_row = date_row.find_next_sibling("tr")
                while next_row and not next_row.get("class"):
                    count += 1
                    next_row = next_row.find_next_sibling("tr")
                # 找到后停止统计
                break
        print('事业编数量',count)
        return count

    except Exception as e:
        return f"事业编访问错误: {str(e)}"
