import time
from io import TextIOWrapper, BufferedReader

import chardet

from utils.data import RjsRandom
from utils.transfer import JsTransfer

class RjsTable(object):
    def setTableName(self,name):
        self.name=name
    def getTableName(self):
        return self.name
    def init_index(self):
        self.indexes={}
    # 创建索引
    def create_index(self, name, keyPath,unique=False):
        if name not in self.indexes:
            self.indexes[name] = {"name": name, "keyPath": keyPath, "options": {"unique": unique}}
    # 创建唯一索引
    def create_index_unique(self,name,keyPath):
        self.create_index(name=name,keyPath=keyPath,unique=True)
    # 创建普通索引
    def create_index_normal(self, name, keyPath):
        self.create_index(name,keyPath,False)
    # 创建主键 唯一索引.
    def setPrimary(self,primary):
        if primary is not None:
            self.primaryKey = str(primary)
            self.create_index_unique('primary_key', primary)
        else:
            self.primaryKey = None
    # 初始化表.
    def setVersion(self,version):
        self.version=str(version)
    def getVersion(self):
        return self.version
    def __init__(self,name,primaryKey=None,autoIncrement=False,version='1',createUniquePrimary=True) -> None:
        self.init_index()
        self.setTableName(str(name))
        self.setPrimary(primaryKey)
        self.autoIncrement=autoIncrement
        self.setVersion(version)
        self.createUniquePrimary=createUniquePrimary

class RjsDatabase():
    def setDbName(self,name):
        self.name=name
    def getDbName(self):
        return self.name
    def setDbVersion(self,version):
        self.version=str(version)
    def getDbVersion(self):
        return self.version

    def addTable(self,table:RjsTable):
        self.tables[table.name]=table
    def has_table(self,table_name):
        return self.get_table(table_name) is not None
    def get_table(self,table_name):
        return self.tables.get(table_name)
    def hasTables(self):
        return len(self.tables)>0

    def get_default_table(self):
        if not self.hasTables():return None
        return list(self.tables.values())[0]
    def get_tables(self):
        return list(self.tables.values())
    def __init__(self,name,version=1,tables:list=None) -> None:
        self.setDbName(name)
        self.setDbVersion(version)
        self.tables={}
        if tables is not None:
            for table in tables:
                self.addTable(table)




class DbStorage:
    ## 初始化 driver和 db name
    def __init__(self, driver,database:RjsDatabase):
        # 初始化容器
        self.database_tables={}
        #
        # 加载 数据库，选择表
        self.driver = driver
        # 工具加载
        self.db_v_name= RjsRandom.random_letter_lower(preffix="RjsDB",length_random=4)
        self.table_v_name= RjsRandom.random_letter_lower(preffix="RjsTableUtils",length_random=4)
        print("DB唯一码:"+self.db_v_name)
        print("TableUtils唯一码:"+self.table_v_name)
        self.jstransfer = JsTransfer(driver)
        self.driver.execute_script(self.jstransfer.data_utils())
        self.driver.execute_script(self.jstransfer.fun_utils())
        #初始化全局数据,异步等待使用
        self.set_database(database)
        if database.hasTables(): self.set_table(database.get_default_table())
        time.sleep(0.5)

    def back2hell(self,hell_key):
        while self.driver.execute_script('return window.RjsData["'+hell_key+'"]') is None:
            print('等待异步回调结果:'+hell_key)
            time.sleep(0.1)
        print('等待结束----获取到返回值----:'+hell_key)
        # 处理 undefined情况
        res = self.driver.execute_script('return window.RjsData["' + hell_key + '"]')
        if res == "rjsUndefined": return None
        return res

    def switch_table(self,table_name:str):
        print('切换表')
        if self.database.has_table(table_name):
            self.table=self.database.get_table(table_name)
    # 设置当前表
    def set_table(self,table:RjsTable):
        # 重设 table,创建table 及主键，基础索引.当前未处理其他索引.
        self.table=RjsTable(name=str(table.name),primaryKey=table.primaryKey,autoIncrement=table.autoIncrement,version=str(table.version),createUniquePrimary=table.createUniquePrimary)
        print('设置表:'+self.table.name)
        js_command = 'window.'+self.db_v_name+'.onupgradeneeded=function(e){var db=window.'+self.db_v_name+'.result;window.'+self.table_v_name+'=db;'+self.get_table_create_js_str()+'};window.'+self.db_v_name+'.onsuccess=function(event){window.'+self.table_v_name+'=event.target.result;var transaction=window.'+self.table_v_name+'.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.count().onsuccess=function(event){window.RjsData[res_token]=event.target.result;console.log("count:",event.target.result)}};window.'+self.db_v_name+'.onerror=function(event){console.log(event.target)};'
        self.table_command= js_command
        #print(js_command)
        self.back2hell(self.driver.execute_script('var res_token=Math.random()+"";'+self.database_command+self.table_command+'return res_token;'))
    def get_table_create_js_str(self):
        create_table_str=''
        if self.database.hasTables():
            for table_1 in self.database.get_tables():
                create_table_str=create_table_str+'var store=db.createObjectStore("' + str(table_1.name) + '"'+('' if table_1.primaryKey is None else ',{'+('keyPath:"'+str(table_1.primaryKey)+'",')+'autoIncrement: '+ ('true' if table_1.autoIncrement else 'false') + '}')+');'+('store.createIndex("primary_key_id_unqiue","'+str(table_1.primaryKey)+'",{unique:true});' if table_1.createUniquePrimary else ';')
        return create_table_str
    def reselect_table(self):
        self.table=None
    # py对象更新 db设置.重新选择表
    def set_database(self,database:RjsDatabase):
        self.database = database
        # self.reselect_table()
        #执行js代码，打开对应版本的数据库
        print('设置数据库:')
        js_command = 'window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB'+";window."+self.db_v_name+"=indexedDB.open('" + str(self.database.name) + "', "+ str(self.database.version) +");"
        #print(js_command)
        self.database_command=js_command
    def __len__(self):
        return self.back2hell(self.driver.execute_script('var res=Math.random()+"";var transaction=window.'+self.table_v_name+'.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.count().onsuccess=function(event){window.RjsData[res]=event.target.result;console.log("success")};return res'))
    # 以map形式返回所有数据
    def items(self):
        dic = {}
        for key in self.keys():
            dic[key] = self.get(key)
        return dic
    def keys(self):
        return self.back2hell(self.driver.execute_script('var res=Math.random()+"";var transaction=window.'+self.table_v_name+'.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.getAllKeys().onsuccess=function(event){window.RjsData[res]=event.target.result;console.log("success")};return res'))

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

    def get(self, key):
        print('get('+key+'):')
        js_command='var res=Math.random()+"";var transaction=window.'+self.table_v_name+'.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.get('+self.pv2jv(key)+').onsuccess=function(event){window.rjs_any_beauty(event.target.result===undefined?"rjsUndefined":event.target.result,res);window.RjsData[res]=event.target.result;console.log("success")};return res'
        #print(js_command)
        return self.back2hell(self.driver.execute_script(js_command))
    def get_all(self):
        print('getAll():')
        dic = {}
        for key in self.keys():
            dic[key] = self.get(key)
        return dic
    # 字典转js字符串  {id:14,name:"小张2",age:"13"}
    def dic2str(self,dic):
        res = '{'
        for key, value in dic.items():
            res = (res if res == '{' else res + ',') + self.pv2jv(key) + ':' + self.pv2jv(value)
        return res + '}'
    def add_all(self, lists):
        for value in lists:
            self.add(value)
    def add(self,tableEntity,key=None):
        entityStr = self.dic2str(tableEntity)
        print('var transaction=window.'+self.table_v_name+'.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.add('+entityStr+('' if key is None else ','+self.pv2jv(key))+').onsuccess=function(event){console.log("success")};')
        self.driver.execute_script('var transaction=window.'+self.table_v_name+'.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.add('+entityStr+('' if key is None else ','+self.pv2jv(key))+').onsuccess=function(event){console.log("success")};')
    def put(self,tableEntity):
        entityStr = self.dic2str(tableEntity)
        self.driver.execute_script('var transaction=window.'+self.table_v_name+'.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.put('+entityStr+').onsuccess=function(event){console.log("success")};')
    # 当不设置主键索引时,使用该方法,或想将indexedDB当作kv方式使用
    def put_kv(self,key,value):
        js_command='var transaction=window.'+self.table_v_name+'.transaction(["' + self.table.name + '"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("' + self.table.name + '");studentsStore.put(window.rjs_beauty_any(' +self.pv2jv(value)+'),'+self.pv2jv(key)+ ').onsuccess=function(event){console.log("success")};'
        print('添加(key-value):'+key)
        # #print(js_command)
        self.driver.execute_script(js_command)
    def put_kv_all(self,kvs):
        for key,value in kvs.items():
            self.put_kv(key,value)
    def has(self, key):
        return self.get(key) is not None
    def remove(self, key):
        self.driver.execute_script('var transaction=window.'+self.table_v_name+'.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.delete('+self.pv2jv(key)+').onsuccess=function(event){console.log("success")};')
    def delete(self, key):
        self.driver.execute_script('var transaction=window.'+self.table_v_name+'.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.delete('+self.pv2jv(key)+').onsuccess=function(event){console.log("success")};')
        return True
    def clear(self):
        self.driver.execute_script('var transaction=window.'+self.table_v_name+'.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.clear().onsuccess=function(event){console.log("success")};')
    # 这个方法暂时不好使
    def drop_table(self):
        self.driver.execute_script('')
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


