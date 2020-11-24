from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from web.LocalStorage import LocalStorage
from web.DbStorage import *
from web.CookieStorage import *
from web.SessionStorage import SessionStorage
from web.Storage import Storage

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.maximize_window()

driver.get("https://www.baidu.com")
# driver.get("http://localhost")

s = Storage(CookieStorage(driver),LocalStorage(driver),SessionStorage(driver),DbStorage(driver,RjsDatabase('blob',2),RjsTable("articles",createUniquePrimary=False)))
# s.save_storage()
# s.load_storage()
# driver.close()