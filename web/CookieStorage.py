import time

from transfer.JsTransfer import JsTransfer


class Cookie:
    def __init__(self, name, value, domain=None, expiry=int(time.time()) + 86400, path='/', secure=True, httpOnly=False,
                 sameSite='None') -> None:
        super().__init__()
        self.name = name
        self.value = value,
        self.domain = domain
        self.path = path
        self.expiry = expiry
        self.secure = secure
        self.httpOnly = httpOnly
        self.sameSite = sameSite


class CookieStorage:

    def __init__(self, driver):
        self.driver = driver
        self.jstransfer = JsTransfer(self.driver)
        self.driver.execute_script(self.jstransfer.data_utils())
        self.driver.execute_script(self.jstransfer.fun_utils())

    def __len__(self):
        return len(self.get_all())

    def items(self):
        return self.get_all()

    def keys(self):
        res = []
        for c1 in self.get_all():
            res.append(c1['name'])
        return res

    def get(self, key):
        return self.driver.get_cookie(key)

    def get_all(self):
        return self.driver.get_cookies()

    def set_all(self, cookies:list):
        for cookie_item in cookies:
            self.set(cookie_item)

    def set_all_strict(self, cookies: list):
        for cookie_item in cookies:
            self.set_strict(cookie_item)

    def set(self, cookie:dict):
        print('-----添加cookie------')
        print(cookie)
        self.driver.add_cookie(cookie)
    def set_strict(self, cookie: Cookie):
        self.driver.add_cookie({'domain': cookie.domain if cookie.domain is not None else self.get_domain(),
                                'expiry': cookie.expiry,
                                'httpOnly': cookie.httpOnly,
                                'name': str(cookie.name),
                                'path': str(cookie.path),
                                'sameSite': cookie.sameSite,
                                'secure': cookie.secure,
                                'value': str(cookie.value)
                                })

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.delete_cookie(key)

    def clear(self):
        self.driver.delete_all_cookies()

    def get_url_root(self):
        url_ps = str(self.driver.current_url).split('/')
        return url_ps[0] + '//' + url_ps[2]

    def get_host(self):
        return str(self.driver.current_url).lstrip('https://').lstrip('http://').split('/')[0]

    def get_domain(self):
        host = self.get_host()
        host_strs = host.split('.')
        domain = host_strs.pop()
        return '.' + host_strs.pop() + '.' + domain

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
