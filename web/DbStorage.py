import time
from io import TextIOWrapper, BufferedReader

import chardet


class RjsDatabase(object):
    def setDbName(self,name):
        self.name=name
    def getDbName(self):
        return self.name
    def setDbVersion(self,version):
        self.version=str(version)
    def getDbVersion(self):
        return self.version

    def __init__(self,name,version=1) -> None:
        self.setDbName(name)
        self.setDbVersion(version)


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

class DbStorage:
    ## 初始化 driver和 db name
    def __init__(self, driver,database:RjsDatabase,table:RjsTable=None):
        # 加载 数据库，选择表
        self.driver = driver
        # 工具加载
        self.driver.execute_script('window.RjsTableUtils=null;window.RjsDB=null;')
        self.driver.execute_script('window.rjs_blobToDataURI=function(blob,res_token){var reader=new FileReader();reader.readAsDataURL(blob);reader.onload=function(e){console.log(e.target.result);if(res_token!==undefined){window.RjsData[res_token]=e.target.result}}};window.rjs_dataURItoBlob=function(base64Data){var byteString;if(base64Data.split(",")[0].indexOf("base64")>=0){byteString=atob(base64Data.split(",")[1])}else{byteString=unescape(base64Data.split(",")[1])}var mimeString=base64Data.split(",")[0].split(":")[1].split(";")[0];var ia=new Uint8Array(byteString.length);for(var i=0;i<byteString.length;i++){ia[i]=byteString.charCodeAt(i)}var blob=new Blob([ia],{type:mimeString});return blob};window.rjs_any_beauty=function(obj,res_token){if(res_token===undefined){res_token=Math.random()+""}if(window.RjsData===undefined){window.RjsData={}}if(obj instanceof Blob){window.rjs_blobToDataURI(obj,res_token)}else{if(typeof obj==="number"){window.RjsData[res_token]=obj}else{if(typeof obj==="boolean"){window.RjsData[res_token]=obj}else{if(typeof obj==="string"){window.RjsData[res_token]=obj}}}}return res_token};window.rjs_beauty_any=function(obj){if(obj instanceof Blob){return obj}else{if(typeof obj==="number"){return obj}else{if(typeof obj==="boolean"){return obj}else{if(typeof obj==="string"){if(obj.indexOf("data:")===0){return window.rjs_dataURItoBlob(obj)}return obj}else{return obj}}}}};')
        #初始化全局数据,异步等待使用
        self.driver.execute_script('window.RjsData={};')
        self.set_database(database)
        if table is not None: self.set_table(table)
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

    # 设置当前表
    def set_table(self,table:RjsTable):
        # 重设 table,创建table 及主键，基础索引.当前未处理其他索引.
        self.table=RjsTable(name=str(table.name),primaryKey=table.primaryKey,autoIncrement=table.autoIncrement,version=str(table.version),createUniquePrimary=table.createUniquePrimary)
        print('设置表:'+self.table.name)
        js_command = 'window.RjsDB.onupgradeneeded=function(e){var db=window.RjsDB.result;window.RjsTableUtils=db;var store=db.createObjectStore("' + str(self.table.name) + '"'+('' if self.table.primaryKey is None else ',{'+('keyPath:"'+str(self.table.primaryKey)+'",')+'autoIncrement: '+ ('true' if self.table.autoIncrement else 'false') + '}')+');'+('store.createIndex("primary_key_id_unqiue","'+str(self.table.primaryKey)+'",{unique:true})};' if self.table.createUniquePrimary else '};')+('window.RjsDB.onsuccess=function(event){window.RjsTableUtils=event.target.result;var transaction=window.RjsTableUtils.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.count().onsuccess=function(event){window.RjsData[res_token]=event.target.result;console.log("count:",event.target.result)}};window.RjsDB.onerror=function(event){console.log(event.target)};')
        self.table_command= js_command
        print(js_command)
        self.back2hell(self.driver.execute_script('var res_token=Math.random()+"";'+self.database_command+self.table_command+'return res_token;'))
        # self.driver.execute_script('window.RjsDB.onsuccess=function(event){window.RjsTableUtils=event.target.result;var transaction=window.RjsTableUtils.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] success!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.count().onsuccess=function(event){console.log("count:",event.target.result)}};')
    def reselect_table(self):
        self.table=None
    # py对象更新 db设置.重新选择表
    def set_database(self,database:RjsDatabase):
        self.database = database
        # self.reselect_table()
        #执行js代码，打开对应版本的数据库
        print('设置数据库:')
        js_command = 'window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB'+";window.RjsDB=indexedDB.open('" + str(self.database.name) + "', "+ str(self.database.version) +");"
        print(js_command)
        self.database_command=js_command
        # self.driver.execute_script('window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB'+";window.RjsDB=indexedDB.open('" + str(self.database.name) + "', "+ str(self.database.version) +");")
    def __len__(self):
        return self.back2hell(self.driver.execute_script('var res=Math.random()+"";var transaction=window.RjsTableUtils.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.count().onsuccess=function(event){window.RjsData[res]=event.target.result;console.log("res:",event.target.result)};return res'))
    # 以map形式返回所有数据
    def items(self):
        dic = {}
        for key in self.keys():
            dic[key] = self.get(key)
        return dic
    def keys(self):
        return self.back2hell(self.driver.execute_script('var res=Math.random()+"";var transaction=window.RjsTableUtils.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.getAllKeys().onsuccess=function(event){window.RjsData[res]=event.target.result;console.log("res:",event.target.result)};return res'))

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
            type = pv.name.split('__rjs__').pop().replace('.', '/')
            if type is None or type == '': type = 'text/plain'
            for line_str in pv.readlines():
                line_str = line_str.replace('\n', '\\n')
                file_str += self.pv2jv(line_str) if file_str == '' else ',' + self.pv2jv(line_str)
            return 'new Blob([' + file_str + '],{"type":' + self.pv2jv(type) + '})'
        elif isinstance(pv, BufferedReader):
            file_str = ''
            type = pv.name.split('__rjs__').pop().replace('.', '/')
            if type is None or type == '': type = 'text/plain'
            encoding = None
            for line_str in pv.readlines():
                if encoding == None: encoding = chardet.detect(line_str)['encoding']
                if encoding == None: encoding = 'utf-8'
                line_str = str(line_str).lstrip('b').strip("'")
                file_str += self.pv2jv(line_str) if file_str == '' else ',' + self.pv2jv(line_str)
            return 'new Blob([' + file_str + '],{"type":' + self.pv2jv(type) + '})'
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
        js_command='var res=Math.random()+"";var transaction=window.RjsTableUtils.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.get('+self.pv2jv(key)+').onsuccess=function(event){window.rjs_any_beauty(event.target.result===undefined?"rjsUndefined":event.target.result,res);console.log("res:",event.target.result)};return res'
        print(js_command)
        return self.back2hell(self.driver.execute_script(js_command))
    def get_all(self):
        dic = {}
        for key in self.keys():
            dic[key] = self.get(key)
        return dic
    # 字典转js字符串  {id:14,name:"小张2",age:"13"}
    def dic2str(self,dic):
        res = '{'
        for key,value in dic.items():
            res=(res if res == '{' else res+',')+str(key)+':'+('"'+value+'"' if isinstance(value,str) else str(value) )
        return res+'}'
    def add_all(self, lists):
        for value in lists:
            self.add(value)
    def add(self,tableEntity,key=None):
        entityStr = self.dic2str(tableEntity)
        print('var transaction=window.RjsTableUtils.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.add('+entityStr+('' if key is None else ','+self.pv2jv(key))+').onsuccess=function(event){console.log("res:",event.target.result)};')
        self.driver.execute_script('var transaction=window.RjsTableUtils.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.add('+entityStr+('' if key is None else ','+self.pv2jv(key))+').onsuccess=function(event){console.log("res:",event.target.result)};')
    def put(self,tableEntity):
        entityStr = self.dic2str(tableEntity)
        self.driver.execute_script('var transaction=window.RjsTableUtils.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.put('+entityStr+').onsuccess=function(event){console.log("res:",event.target.result)};')
    # 当不设置主键索引时,使用该方法,或想将indexedDB当作kv方式使用
    def put_kv(self,key,value):
        js_command='var transaction=window.RjsTableUtils.transaction(["' + self.table.name + '"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("' + self.table.name + '");studentsStore.put(window.rjs_beauty_any(' +self.pv2jv(value)+'),'+self.pv2jv(key)+ ').onsuccess=function(event){console.log("res:",event.target.result)};'
        print('添加(key-value):'+key)
        print(js_command)
        self.driver.execute_script(js_command)
    def has(self, key):
        return self.get(key) is not None
    def remove(self, key):
        self.driver.execute_script('var transaction=window.RjsTableUtils.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.delete('+self.pv2jv(key)+').onsuccess=function(event){console.log("res:",event.target.result)};')
    def delete(self, key):
        self.driver.execute_script('var transaction=window.RjsTableUtils.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.delete('+self.pv2jv(key)+').onsuccess=function(event){console.log("res:",event.target.result)};')
        return True
    def clear(self):
        self.driver.execute_script('var transaction=window.RjsTableUtils.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.clear().onsuccess=function(event){console.log("res:",event.target.result)};')
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


