class JsUtils:

    def __init__(self, driver):
        self.driver = driver

    def __len__(self):
        return 1

    def alert(self, str):
        self.driver.execute_script('window.alert("' + str + '")')

    def log(self, str):
        self.driver.execute_script('window.console.log("' + str + '")')

    def snap_shot(self):
        self.log('保存当前链接,缓存数据等')

    def snap_shot_store(self):
        self.log('这里只包婚缓存数据')
