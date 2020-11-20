import time


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
        self.driver.execute_script('window.RjsTableUtils=null;window.RjsDB=null;')
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
        js_command = 'window.RjsDB.onupgradeneeded=function(e){var db=window.RjsDB.result;window.RjsTableUtils=db;var store=db.createObjectStore("' + str(self.table.name) + '"'+('' if self.table.primaryKey is None else ',{'+('keyPath:"'+str(self.table.primaryKey)+'",')+'autoIncrement: '+ ('true' if self.table.autoIncrement else 'false') + '}')+');'+('store.createIndex("primary_key_id_unqiue","'+str(self.table.primaryKey)+'",{unique:true})};' if self.table.createUniquePrimary else '};')+('window.RjsDB.onsuccess=function(event){window.RjsTableUtils=event.target.result;var transaction=window.RjsTableUtils.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.count().onsuccess=function(event){console.log("count:",event.target.result)}};window.RjsDB.onerror=function(event){console.log(event.target)};')
        self.table_command= js_command
        print(js_command)
        self.driver.execute_script(self.database_command+self.table_command)
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
        self.driver.execute_script('window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB'+";window.RjsDB=indexedDB.open('" + str(self.database.name) + "', "+ str(self.database.version) +");")
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
       return '"' + pv + '"' if isinstance(pv, str) else str(pv)
    def get(self, key):
        return self.back2hell(self.driver.execute_script('var res=Math.random()+"";var transaction=window.RjsTableUtils.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.get('+self.pv2jv(key)+').onsuccess=function(event){window.RjsData[res]=event.target.result===undefined?"rjsUndefined":event.target.result;console.log("res:",event.target.result)};return res'))
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
    def put_kv(self,key,value):
        self.driver.execute_script(
            'var transaction=window.RjsTableUtils.transaction(["' + self.table.name + '"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("' + self.table.name + '");studentsStore.put(' +self.pv2jv(value)+','+self.pv2jv(key)+ ').onsuccess=function(event){console.log("res:",event.target.result)};')
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


