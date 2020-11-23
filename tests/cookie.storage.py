from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from web.LocalStorage import LocalStorage
from web.DbStorage import *
from web.CookieStorage import *
driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.maximize_window()

driver.get("https://www.baidu.com")
print('-----------getAll()---------')
print(driver.get_cookies())
print('-------cookies----------')
cs= CookieStorage(driver)
driver.add_cookie({'domain': '.baidu.com',"hhhhhh":"hhhhhHHHH", 'expiry': 1637660470, 'httpOnly': False, 'name': 'BAIDUID_BFESS', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '284F89D3FB52E641AFAB37BAD4D9E31E:FG=1'})


print('-------------keys()-----------')
print(cs.keys())
print('-----------getAll()---------')
print(driver.get_cookies())

driver.close()



print('---------------over----------------')