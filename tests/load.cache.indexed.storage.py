from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from web.LocalStorage import LocalStorage
from web.DbStorage import *

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.maximize_window()

driver.get("https://www.baidu.com")

# db = DbStorage(driver,RjsDatabase(name='localforage',version=2),RjsTable(name='keyvaluepairs',createUniquePrimary=False))









driver.minimize_window()



print('---------------over----------------')