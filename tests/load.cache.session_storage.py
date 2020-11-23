from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from web.LocalStorage import LocalStorage
from web.DbStorage import *
from web.SessionStorage import SessionStorage

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.maximize_window()

driver.get("https://www.baidu.com")

#-----------------------------------------------------------------------------
ss= SessionStorage(driver)
ss.set('ss_key1bool',True)
ss.set('str','ahah哈哈,.- s')
ss.set('ints',1234)
ss.set('map',{"type":"jxxx","xxx":False,"fan":123,"mm":{"K":1,"b":True}})
print(ss.get('ss_key1bool'))
print(ss.get('map'))
print('getAll():')
print(ss.get_all())
print(ss.keys())
print(str(len(ss)))
print('keys():')
print(ss.keys())
print('-----')
print(ss.get('map'))
print('items:')
print(ss.items())




#------------------------------------------------------------------------------
driver.close()



print('---------------over----------------')