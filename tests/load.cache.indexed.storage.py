from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from web.LocalStorage import LocalStorage
from web.DbStorage import *

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.maximize_window()

driver.get("https://www.baidu.com")

db = DbStorage(driver,RjsDatabase(name='localforage',version=2),RjsTable(name='keyvaluepairs',createUniquePrimary=False))
db.put_kv('boo',True)
db.put_kv('num',123)
db.put_kv('str','哈哈哈哈aabbj123,. s')
db.put_kv('dic',{"k":"v","k1":1,"dic":{"d":12,"c":False}})
# print(db.get_all())
print(db.get('dic'))







driver.minimize_window()



print('---------------over----------------')