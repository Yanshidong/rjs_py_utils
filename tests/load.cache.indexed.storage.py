from selenium import webdriver
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from web.LocalStorage import LocalStorage
from web.DbStorage import *

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.maximize_window()

driver.get("https://element.eleme.cn/#/zh-CN")

# db = DbStorage(driver,RjsDatabase(name='localforage',version=2),RjsTable(name='keyvaluepairs',createUniquePrimary=False))
# # print(db.get_all())
# db.put_kv_all({
# 'boo':True,
# 'num':123,
# 'str':'哈哈哈哈aabbj123,. s',
# 'dic':{"k":"v","k1":1,"dic":{"d":12,"c":False}}
# })
# print(db.get_all())
#
#
#
#
#
#
#
# driver.close()



print('---------------over----------------')


