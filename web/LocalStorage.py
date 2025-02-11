from utils.transfer import JsTransfer
class LocalStorage:

    def __init__(self, driver):
        self.driver = driver
        self.jstransfer=JsTransfer(self.driver)
        print('---init----')
        print(self.jstransfer.data_utils())
        self.driver.execute_script(self.jstransfer.data_utils())
        print(self.jstransfer.fun_utils())
        self.driver.execute_script(self.jstransfer.fun_utils())

    def __len__(self):
        return self.driver.execute_script("return window.localStorage.length;")

    def items(self):
        return self.driver.execute_script( \
            "var ls = window.localStorage, items = {}; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  items[k = ls.key(i)] = ls.getItem(k); " \
            "return items; ")

    def keys(self):
        return self.driver.execute_script( \
            "var ls = window.localStorage, keys = []; " \
            "for (var i = 0; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)

    def get_all(self):
        dic = {}
        for key in self.keys():
            dic[key] = self.get(key)
        return dic

    def set_all(self, maps):
        for key, value in maps.items():
            self.set(key, value)

    def set(self, key, value):
        js_command='window.localStorage.setItem('+self.jstransfer.pv2jv(key)+','+self.jstransfer.pv2jv(value)+');'
        print('set:'+key)
        print(js_command)
        self.driver.execute_script(js_command)

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
