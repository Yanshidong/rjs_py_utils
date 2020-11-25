import os

from web.CookieStorage import CookieStorage
from web.DbStorage import DbStorage, RjsTable
from web.LocalStorage import LocalStorage
from web.SessionStorage import SessionStorage
import pickle

class Storage:
    # 判断是否已经缓存过
    # @Return Bool
    def has_cache(self):
        return os.path.exists(self.cs_all_file_name) and os.path.exists(self.ls_all_file_name) and os.path.exists(self.ss_all_file_name)
    def save_if_not_exits(self):
        if not self.has_cache():
            print('----未检测到缓存文件:执行保存操作----')
            self.save_storage()
            self.save_db()
    def load_if_exits(self):
        if self.has_cache():
            print('----检测到存在缓存:加载缓存操作----')
            self.load_storage()
            self.load_db()
    def __init__(self,cs:CookieStorage,ls:LocalStorage,ss:SessionStorage,db:DbStorage) -> None:
        self.base_path=self.make_dir_exist('./tmp')
        self.cs_all_file_name=self.base_path+'/cookie_all.pckl'
        self.ss_all_file_name=self.base_path+'/session_all.pckl'
        self.ls_all_file_name=self.base_path+'/local.pckl'
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
    def make_dir_exist(self,dir_path:str):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path

    def get_keys_in_dir(self,dir_path:str):
        keys_list=[]
        for root, dirs, files in os.walk(dir_path):
            for fi in files:
                keys_list.append(fi.replace('__rjs__','/'))
        return keys_list
    def save_table(self,table_obj:RjsTable):
        self.db.switch_table(table_obj.name)
        table_name=self.db.table.name
        table_path=self.make_dir_exist(self.base_path+'/'+table_name)
        for key_1 in self.db.keys():
            f_key_name=key_1.replace('/','__rjs__')
            self.file_push(self.db.get(key_1),table_path+'/'+f_key_name)
    def save_db(self):
        for table_1 in self.db.database.get_tables():
            self.save_table(table_1)
    def load_table(self,table:RjsTable):
        self.db.switch_table(table.name)
        table_path=self.base_path+'/'+self.db.table.name
        # 获得 keys,
        for key_1 in self.get_keys_in_dir(table_path):
            print('----加载缓存-key:'+key_1+'-----')
            self.db.put_kv(key_1,self.file_pull(table_path+'/'+(key_1.replace('/','__rjs__'))))
    def load_db(self):
        for table_1 in self.db.database.get_tables():
            self.load_table(table_1)
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