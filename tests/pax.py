from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains

from web.CookieStorage import CookieStorage
from web.LocalStorage import LocalStorage
from web.DbStorage import *

#定义一个空字典传入遍历结果
from web.SessionStorage import SessionStorage
from web.Storage import Storage

wardrobe_combination ={}

#进入pax系统，选择BU与商场
driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.maximize_window() #最大化窗口
driver.get("http://pax-design-tool-sit.aidesign.ingka-dt.cn")  # 地址栏里输入网址
# 读取缓存,写入,并跳转到Homepage
# s = Storage(CookieStorage(driver),LocalStorage(driver),SessionStorage(driver),DbStorage(driver,RjsDatabase('localforage',2),RjsTable("keyvaluepairs",createUniquePrimary=False)))
# s.load_storage()

time.sleep(10)
driver.find_element_by_css_selector(
    "#root > div > div.wrap > div.choose-store > section.store-setting-area > div > div:nth-child(1) > div.ant-select.ant-select-enabled").click()  # 定位国家选择
time.sleep(2)
driver.find_element_by_xpath("//li[contains(.,'中国')]").click()  # 选择中国
time.sleep(2)
driver.find_element_by_css_selector(
    "#root > div > div.wrap > div.choose-store > section.store-setting-area > div > div:nth-child(2) > div.ant-select.ant-select-enabled > div").click()  # 定位门店选择狂
time.sleep(2)
driver.find_element_by_xpath("//li[contains(.,'无锡商场 164')]").click()  # 选择无锡商场
time.sleep(3)
driver.find_element_by_class_name("next").click()#点击下一步

### post token   谢日
# localStorage =LocalStorage(driver)
# localStorage.get_all()
# localStorage.set("TOKEN",localStorage.get_token())

# 获取当前的URL
def url_contains(str):
    current_ur = driver.current_url
    return str in current_ur

#添加等待
def wait_2_second(waited_time):
    time.sleep(2)
    waited_time += 2
    return waited_time

#打印等待日志
def wait_2_second_check_exit_flag(waited_time, log=''):
    print(log + ',倒计时2s,已等待:' + str(waited_time) + 's')
    time = wait_2_second(waited_time)
    return time

#检测是否进入homepage页
def ready_homepage():
    print('检测 homepage')
    wait_time = 0
    while not url_contains('/homepage') :
        wait_time = wait_2_second_check_exit_flag(wait_time, '等待进入homepage')

#检测是否进入wardrobe_type_page页
def ready_select_wardrobe_type_page():
    print('检测 wardrobe_type_page')
    wait_time = 0
    while not url_contains('/choose-wardrobe-type') :
        wait_time = wait_2_second_check_exit_flag(wait_time, '等待进入choose-wardrobe-type')

#遍历柜体组合
def ok_wardrobe_result(doortype,width,height,depth,color):
    bianli = driver.find_elements_by_class_name("select-item-btn")#生成柜体组合的list
    person = driver.find_elements_by_css_selector(
        "div.wrap > div.recommend-straight-plan-web > div.side-bar > div > div.clothing-view.marb60 > div.marb40.ant-row > div:nth-child(2) > ul > li")
    person = len(person)
    for wardrobe in bianli:
        print(wardrobe.text)
        wardrobe.click()#遍历点击返回的list
        person = driver.find_elements_by_css_selector(
            "div.wrap > div.recommend-straight-plan-web > div.side-bar > div > div.clothing-view.marb60 > div.marb40.ant-row > div:nth-child(2) > ul > li")
        person = len(person)
        for index_person in range(person):
            person = driver.find_elements_by_css_selector(
                "div.wrap > div.recommend-straight-plan-web > div.side-bar > div > div.clothing-view.marb60 > div.marb40.ant-row > div:nth-child(2) > ul > li")[index_person]
            person.click()
            time.sleep(3)
            card = driver.find_elements_by_class_name('wardrobe-card')#找到推荐结果的元素
            time.sleep(3)
            person.click()
            time.sleep(2)




        #如果card数量大于0，则返回了推荐结果，若不大于0，则未返回推荐结果
            if len(card)>0:
               write_txt("门型："+ str(doortype) +"，" + "宽度：" + str (width)+"，" + "高度：" +str(height)+"，" + "深度：" + str(depth)+"，"+ "颜色：" + str(color)+"，" +
                         "柜体组合：" + wardrobe.text + '，' + ' 储物需求：' + str(person.text) + '，' + "返回衣柜数量：" + str(len(card)) +
                         ", 结果：ok √," + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
            else:
               write_txt("门型："+ str(doortype) +"，" + "宽度：" + str (width)+"，" + "高度：" +str(height)+"，" + "深度：" + str(depth)+"，"+ "颜色：" + str(color)+"，" +
                         "柜体组合：" + wardrobe.text + '，' + ' 储物需求：' + str(person.text) + '，'  + "返回衣柜数量：" + str(len(card))+
                         ", 结果：裂开 ×," + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))) #and driver.get_screenshot_as_png(r'C:\Users\qisun\Desktop\pax')  #截图到指定路径

#写入txt文件
def write_txt(a1):
    test_result = "test_result.txt"
    with open(test_result, "a") as file:  # w为覆盖，代表追加内容a
        file.write(a1+"\n")
        file.close()


#点击设计衣柜
ready_homepage()
s = Storage(CookieStorage(driver),LocalStorage(driver),SessionStorage(driver),DbStorage(driver,RjsDatabase('localforage',2),RjsTable("keyvaluepairs",createUniquePrimary=False)))
time.sleep(3)
print('点击设计衣柜')
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div/span').click()#点击立柜设计

#选择立柜设计
ready_select_wardrobe_type_page()
print('选择立柜')
time.sleep(3)
ActionChains(driver).move_by_offset(830,537).click().perform() #通过坐标定位点击
ActionChains(driver).move_by_offset(-830,-537).perform() #将坐标回溯

#定义一个靠坐标点击的方法，点击完成后坐标回溯
def action_move_click1(x,y):
    ActionChains(driver).move_by_offset(x,y).click().perform()  # 通过坐标定位点击
    ActionChains(driver).move_by_offset(-x, -y).perform()  # 将坐标回溯



#获取宽度坐标并且进行遍历
def location_width():
    oo = []
    door_width = driver.find_elements_by_class_name("ant-slider-dot")
    for dot in door_width:
        dot.location
        oo.append([dot.location['x'],dot.location['y']+115])
    return [oo]

# document.getElementsByTagName('body')[0].onclick=function(event){
#  console.log("clicked at("+event.clientX+","+event.clientY+")");
# };                             在consle获取坐标

huamen_width_location = [
    [689,389],
    [825,393],
    [1103,391],
    [1372,391]



]

heyemen_width_location = [
    [689,390],
    [735,391],
    [786,387],
    [836,389],
    [879,387],
    [937,393],
    [987,391],
    [1029,391],
    [1077,392],
    [1131,389],
    [1173,389],
    [1273,388],
    [1374,390]
]
# driver.execute_script('document.querySelectorAll("div.wardrobeSize > div > div > div > div.main-content > div:nth-child(1) > section > button")')执行js
#遍历组合场景
time.sleep(5)
doortype = driver.find_elements_by_css_selector('div.wardrobeSize > div > div > div > div.main-content > div:nth-child(1) > section > button')
total = len(doortype)
print(total)
for index_doortype in range(total):
    doortype = driver.find_elements_by_css_selector('div.wardrobeSize > div > div > div > div.main-content > div:nth-child(1) > section > button')[index_doortype]
    doortype.click()
    width = []
    if "滑门" in doortype.text or "Sliding" in doortype.text:
        width = huamen_width_location
    else:
        width = heyemen_width_location
    for index_width in width:
        action_move_click1(index_width[0], index_width[1])
        height = driver.find_elements_by_css_selector("div.wardrobeSize > div > div > div > div.main-content > div:nth-child(3) > section>button")
        height = len(height)
        for index_height in range(height):
            height = driver.find_elements_by_css_selector("div.wardrobeSize > div > div > div > div.main-content > div:nth-child(3) > section>button")[index_height]
            height.click()
            depth = driver.find_elements_by_css_selector("div.wardrobeSize > div > div > div > div.main-content > div:nth-child(4) > section > button")
            depth = len(depth)
            for index_depth in range(depth):
                depth = driver.find_elements_by_css_selector("div.wardrobeSize > div > div > div > div.main-content > div:nth-child(4) > section > button")[index_depth]
                depth.click()
                color = driver.find_elements_by_css_selector("div.wrap > div.wardrobeSize > div > div > div > div.main-content > div.form-item.small.zh-CN > div > div > label.ant-radio-wrapper")
                color = len(color)
                for index_color in range(color):
                    color = driver.find_elements_by_css_selector("div.wrap > div.wardrobeSize > div > div > div > div.main-content > div.form-item.small.zh-CN > div > div > label.ant-radio-wrapper")[index_color]
                    color.click()
                    height_log = height.text
                    depth_log = depth.text
                    doortype_log = doortype.text
                    select_one_color = color.get_attribute("class")
                    color_log = str(select_one_color).split().pop()
                    driver.find_element_by_css_selector("#root > div > div.wrap > div.wardrobeSize > div > div > div > div.confirm-btn > button").click()#点击确定按钮
                    time.sleep(5)
                    width_value = driver.find_element_by_css_selector("#root > div > div.wrap > div.wardrobeSize > div > div > div > div.main-content > div:nth-child(2) > div > div > div.ant-slider-handle").get_attribute("aria-valuenow")
                    ok_wardrobe_result(doortype_log,width_value,height_log,depth_log,color_log)
                    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/i').click()
                    time.sleep(3)







