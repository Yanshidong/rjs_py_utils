from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from web.LocalStorage import LocalStorage
from web.DbStorage import *
from web.CookieStorage import *
driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.maximize_window()

driver.get("https://www.baidu.com")

print('-------cookies----------')
cs= CookieStorage(driver)
driver.add_cookie({"hahahahha":"this is value"})



print('-----------getAll()---------')
print(driver.get_cookies())

driver.close()



print('---------------over----------------')