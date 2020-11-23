from io import TextIOWrapper, BufferedReader

import chardet


class SessionStorage:

    def __init__(self, driver):
        self.driver = driver

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
        self.driver.execute_script("window.sessionStorage.setItem(arguments[0], arguments[1]);", key, self.pv2jv(value))

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script("window.sessionStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("window.sessionStorage.clear();")
    def pv2jv(self,pv):
        if isinstance(pv, bool):
            return 'true' if pv else 'false'
        elif isinstance(pv, int):
            return str(pv)
        elif isinstance(pv, float):
            return str(pv)
        elif isinstance(pv, str):
            return '"' + (pv.replace('"', '\\"')) + '"'
        elif isinstance(pv, TextIOWrapper):
            file_str = ''
            type_f = pv.name.split('__rjs__').pop().replace('.', '/')
            if type_f is None or type_f == '': type_f = 'text/plain'
            for line_str in pv.readlines():
                line_str = line_str.replace('\n', '\\n')
                file_str += self.pv2jv(line_str) if file_str == '' else ',' + self.pv2jv(line_str)
            return 'new Blob([' + file_str + '],{"type":' + self.pv2jv(type_f) + '})'
        elif isinstance(pv, BufferedReader):
            file_str = ''
            type_f = pv.name.split('__rjs__').pop().replace('.', '/')
            if type_f is None or type_f == '': type_f = 'text/plain'
            encoding = None
            for line_str in pv.readlines():
                if encoding == None: encoding = chardet.detect(line_str)['encoding']
                if encoding == None: encoding = 'utf-8'
                line_str = str(line_str).lstrip('b').strip("'")
                file_str += self.pv2jv(line_str) if file_str == '' else ',' + self.pv2jv(line_str)
            return 'new Blob([' + file_str + '],{"type":' + self.pv2jv(type_f) + '})'
        elif isinstance(pv, set):
            return str(pv)
        elif isinstance(pv, tuple):
            return str(tuple)
        elif type(pv).__name__ == 'dict':
            return self.dic2str(pv)
        elif isinstance(pv, list):
            res = ''
            for v1 in pv:
                res = res +(self.pv2jv(v1) if res=='' else ','+self.pv2jv(v1))
            return '['+res+']'

    def dic2str(self, dic):
        res = '{'
        for key, value in dic.items():
            res = (res if res == '{' else res + ',') + self.pv2jv(key) + ':' + self.pv2jv(value)
        return res + '}'
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
