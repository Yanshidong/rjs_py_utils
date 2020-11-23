from transfer.JsTransfer import JsTransfer
class CookieStorage:

    def __init__(self, driver):
        self.driver = driver
        self.jstransfer=JsTransfer(self.driver)
        self.driver.execute_script(self.jstransfer.data_utils())
        self.driver.execute_script(self.jstransfer.fun_utils())

    def __len__(self):
        return len(self.driver.get_cookies())

    def items(self):
        return self.driver.self.driver.get_cookies()

    def keys(self):
        return self.driver.execute_script( \
            "var ls = window.localStorage, keys = []; " \
            "for (var i = 0; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.get_cookie(key)

    def get_all(self):
        return self.driver.self.driver.get_cookies()

    def set_all(self, maps):
        for key, value in maps.items():
            self.set(key, value)

    def set(self, key, value):
        self.driver.execute_script('window.localStorage.setItem('+self.jstransfer.pv2jv(key)+','+self.jstransfer.pv2jv(value)+');')

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script("window.localStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("window.localStorage.clear();")

    def __getitem__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.items().__iter__()

    def __repr__(self):
        return self.items().__str__()
