from io import TextIOWrapper, BufferedReader

import chardet
from transfer.JsTransfer import JsTransfer

class SessionStorage:

    def __init__(self, driver):
        self.driver = driver
        self.jstransfer=JsTransfer(driver)
        self.driver.execute_script(self.jstransfer.data_utils())
        self.driver.execute_script(self.jstransfer.fun_utils())

    def __len__(self):
        return self.driver.execute_script("return window.sessionStorage.length;")

    def items(self):
        return self.driver.execute_script( \
            "var ls = window.sessionStorage, items = {}; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  items[k = ls.key(i)] = ls.getItem(k); " \
            "return items; ")

    def keys(self):
        return self.driver.execute_script( \
            "var ls = window.sessionStorage, keys = []; " \
            "for (var i = 0; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script("return window.sessionStorage.getItem(arguments[0]);", key)

    def get_all(self):
        dic = {}
        for key in self.keys():
            dic[key] = self.get(key)
        return dic

    def set_all(self, maps):
        for key, value in maps.items():
            self.set(key, value)

    def set(self, key, value):
        self.driver.execute_script('window.sessionStorage.setItem('+self.pv2jv(key)+', '+self.pv2jv(value)+');')

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script("window.sessionStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("window.sessionStorage.clear();")
    def pv2jv(self,pv):
        return self.jstransfer.pv2jv(pv)

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
