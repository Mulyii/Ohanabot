import requests
from selenium import webdriver
from lxml import etree
from time import sleep
import re
import random
from selenium.webdriver.common.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_html(html):
    tree = etree.HTML(html)
	
    prob_urls = tree.xpath('//*[@id="pageContent"]//*[@class="datatable"]//*[@class="status-frame-datatable"]/tbody/tr/td[4]/a/@href') # 题目链接
    status = tree.xpath('//*[@id="pageContent"]//*[@class="datatable"]//*[@class="status-frame-datatable"]/tbody/tr/td[6]/span/span/text()') # 测评信息

    for prob, sta in zip(prob_urls, status):
        with open('test.txt', 'a', encoding = 'utf8') as f:
            prob = str(prob)
            f.write('题目url：' + prob + '\n' +
                    '状态：' + sta + '\n' + '\n')

def ask_codeforce(user: str, prob: str):
    chrome_driver = '../driver/chromedriver_win32.exe'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('disable-infobars')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome = webdriver.Chrome(options = options, executable_path = chrome_driver)
    chrome.get(f"https://codeforces.com/submissions/{user}")
    print("完成浏览器打开任务")
    # 等待10秒钟，直到页面中id为my-element的元素加载完成
    element = WebDriverWait(chrome, 10).until(
        EC.presence_of_element_located((By.ID, "pageContent"))
    )
    print("页面加载完成")
    html = chrome.page_source
    parse_html(html)


if __name__ == '__main__':
    ask_codeforce("WinterLove", "")