# 导入requests库
import requests
# 设置请求头，模拟浏览器访问
def codeforces_contests() :
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }
    # 设置比赛的url
    url = 'https://codeforces.com/contests?complete=true'
    # 发送get请求，获取网页内容
    response = requests.get(url=url, headers=headers)
    # 判断响应状态码是否为200（成功）
    if response.status_code == 200:
        # 获取网页源码
        html = response.text
        # 使用pyquery库解析网页源码
        from pyquery import PyQuery as pq
        # 创建pyquery对象
        doc = pq(html)
        # 获取比赛信息所在的表格元素（通过css选择器）
        table = doc('.contestList').remove('.contests-table')
        # 获取表格中的每一行元素（通过css选择器）
        rows = table('tr')
        # 遍历每一行元素（跳过第一行表头）
        
        res = ""
        for row in rows[1:]:
            # 创建pyquery对象
            row = pq(row)
            # 获取比赛名称所在的单元格元素（通过css选择器）
            name_cell = row('td:nth-child(1)')
            # 获取比赛名称文本（去除空白字符）
            name_text = name_cell.text().strip()
            # 获取比赛时间所在的单元格元素（通过css选择器）
            time_cell = row('td:nth-child(3)')
            # 获取比赛时间文本（去除空白字符）
            time_text = time_cell.text().strip()
            # 打印比赛名称和时间
            # print(id_cell, name_text, time_text)
            res += "{}\n{}\n".format(name_text, time_text)
        return res
