from web.CookieStorage import CookieStorage
from web.DbStorage import DbStorage
from web.LocalStorage import LocalStorage
from web.SessionStorage import SessionStorage
import pickle

class Storage:
    def __init__(self,cs:CookieStorage,ls:LocalStorage,ss:SessionStorage,db:DbStorage) -> None:
        self.cs_all_file_name='./tmp/cookie_all.pckl'
        self.ss_all_file_name='./tmp/session_all.pckl'
        self.ls_all_file_name='./tmp/local.pckl'
        self.cs=cs
        self.ls=ls
        self.ss=ss
        self.db=db
    def file_push(self,data,file_name):
        f = open(file_name, 'wb')
        pickle.dump(data, f)
        f.close()
    def file_pull(self,file_name):
        f = open(file_name, 'rb')
        res=pickle.load(f)
        f.close()
        return res
    def save_cookie(self):
        cs_data= self.cs.get_all()
        self.file_push(cs_data,self.cs_all_file_name)
    def save_session_storage(self):
        ss_data= self.ss.get_all()
        self.file_push(ss_data,self.ss_all_file_name)
    def save_local_storage(self):
        self.file_push(self.ls.get_all(),self.ls_all_file_name)
    def load_cookie(self):
        cs_data=self.file_pull(self.cs_all_file_name)
        self.cs.set_all(cs_data)
    def load_session_storage(self):
        ss_data=self.file_pull(self.ss_all_file_name)
        self.ss.set_all(ss_data)
    def load_local_storage(self):
        ls_data=self.file_pull(self.ls_all_file_name)
        self.ls.set_all(ls_data)
    def save_storage(self):
        self.save_cookie()
        self.save_local_storage()
        self.save_session_storage()
    def load_storage(self):
        self.load_cookie()
        self.load_local_storage()
        self.load_session_storage()