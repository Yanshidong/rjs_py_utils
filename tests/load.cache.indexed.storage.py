from selenium import webdriver
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from web.LocalStorage import LocalStorage
from web.DbStorage import *

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.maximize_window()

driver.get("https://www.baidu.com")

db = DbStorage(driver,RjsDatabase('localforage',2,[RjsTable(name='keyvaluepairs',createUniquePrimary=False),RjsTable(name='local-forage-detect-blob-support',createUniquePrimary=False)]))
print(db.get_all())
db.put_kv_all({
'boo':True,
'num':123,
'str':'哈哈哈哈aabbj123,. s',
'dic':{"k":"v","k1":1,"dic":{"d":12,"c":False}}
})
print('-------------all 1')
print(db.get_all())
db.switch_table('local-forage-detect-blob-support')
db.put_kv_all({
'boo':True,
'dic':{"k":"v","k1":1,"dic":{"d":12,"c":False}}
})
print('--------------all 2')
print(db.get_all())
#
#
#
#
#
#
#
driver.close()


print('---------------over----------------')


