from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from web.LocalStorage import LocalStorage
from web.DbStorage import *

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.maximize_window()

driver.get("https://www.baidu.com")

ls=LocalStorage(driver)
ls.set_all({'wwwPassLogout': '0', 'bool': 'true', 'BIDUPSID': '1AD83F7E9E88BC56CCFE6524AEA72517', 'str': 'i am a', 'map': '[object Object]', 'safeIconHis': '', 'int': '123'})
print('getAll():')
print(ls.get_all())


# driver.close()











print('---------------over----------------')