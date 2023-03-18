import time
from selenium import webdriver
driver = webdriver.Chrome("../driver/chromedriver_win32.exe")
driver.get("https://www.baidu.com/")
time.sleep(5)
