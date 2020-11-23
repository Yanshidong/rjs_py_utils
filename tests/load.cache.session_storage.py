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
ss.set_all({'ints': '1234', 'str': 'ahah哈哈,.- s', 'ss_key1bool': 'true'})
print('getAll():')
print(ss.get_all())




#------------------------------------------------------------------------------
driver.close()



print('---------------over----------------')