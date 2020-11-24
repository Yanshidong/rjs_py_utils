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
driver.add_cookie({'domain': '.baidu.com', 'expiry': 1637660470, 'httpOnly': False, 'name': 'Rjs_token', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '284F89D3FB52E641AFAB37BAD4D9E31E:FG=1'})


print('-------------keys()-----------')
print(cs.keys())
print('-----------getAll()---------')
print(cs.get_all())
print('----------get_host')
print(cs.get_host())
print('----------get_domain')
print(cs.get_domain())
print('----------get_root_url')
print(cs.get_url_root())
print('--------len------------')
print(len(cs))
print('--------clear-------')
cs.clear()
print('----------len--------')
print(len(cs))
print('---------添加一批')
# driver.add_cookie({'domain': '.baidu.com', 'expiry': 1637660470, 'httpOnly': False, 'name': 'Rjs_token', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '284F89D3FB52E641AFAB37BAD4D9E31E:FG=1'})
cs.set_all([{'domain': '.baidu.com', 'expiry': 1637660470, 'httpOnly': False, 'name': 'Rjs_token', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '284F89D3FB52E641AFAB37BAD4D9E31E:FG=1'}, {'domain': '.baidu.com', 'expiry': 1637719209, 'httpOnly': False, 'name': 'BAIDUID_BFESS', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'AA251F9164D285B81E4640D9D2751156:FG=1'}, {'domain': '.baidu.com', 'httpOnly': False, 'name': 'H_PS_PSSID', 'path': '/', 'secure': False, 'value': '32817_1448_32856_33058_31660_33099_33101_32962'}, {'domain': '.baidu.com', 'expiry': 1637719208, 'httpOnly': False, 'name': 'BAIDUID', 'path': '/', 'secure': False, 'value': 'AA251F9164D285B81E4640D9D2751156:FG=1'}, {'domain': '.baidu.com', 'expiry': 3753666855, 'httpOnly': False, 'name': 'BIDUPSID', 'path': '/', 'secure': False, 'value': 'AA251F9164D285B8C642DC5EB355BDF7'}, {'domain': '.baidu.com', 'expiry': 3753666855, 'httpOnly': False, 'name': 'PSTM', 'path': '/', 'secure': False, 'value': '1606183208'}, {'domain': 'www.baidu.com', 'expiry': 1607047211, 'httpOnly': False, 'name': 'BD_UPN', 'path': '/', 'secure': False, 'value': '12314753'}, {'domain': 'www.baidu.com', 'httpOnly': False, 'name': 'BD_HOME', 'path': '/', 'secure': False, 'value': '1'}])
print('----get_all()-----')
print(cs.get_all())
driver.close()

print('---------------over----------------')