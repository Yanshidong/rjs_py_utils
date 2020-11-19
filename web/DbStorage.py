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
        self.primaryKey=primary
        self.create_index_unique('primary_key',primary)
    # 初始化表.
    def setVersion(self,version):
        self.version=str(version)
    def getVersion(self):
        return self.version
    def __init__(self,name,primaryKey,autoIncrement=False,version='1') -> None:
        self.init_index()
        self.setTableName(str(name))
        self.setPrimary(str(primaryKey))
        self.autoIncrement=autoIncrement
        self.setVersion(version)

class DbStorage:
    ## 初始化 driver和 db name
    def __init__(self, driver,database:RjsDatabase,table:RjsTable=None):
        # 加载 数据库，选择表
        self.driver = driver
        self.driver.execute_script('window.RjsTableUtils=null;window.RjsDB=null;')
        self.set_database(database)
        if table is not None: self.set_table(table)
    # 设置当前表
    def set_table(self,table:RjsTable):
        # 重设 table,创建table 及主键，基础索引.当前未处理其他索引.
        self.table=RjsTable(name=str(table.name),primaryKey=str(table.primaryKey),autoIncrement=table.autoIncrement,version=str(table.version))
        self.driver.execute_script('window.RjsDB.onupgradeneeded=function(e){var db=window.RjsDB.result;window.RjsTableUtils=db;var store=db.createObjectStore("' + str(self.table.name) + '",{keyPath:"'+str(self.table.primaryKey)+'",autoIncrement: '+ ('true' if self.table.autoIncrement else 'false') + '});store.createIndex("student_id_unqiue","'+str(self.table.primaryKey)+'",{unique:true})};')
        # self.driver.execute_script('window.RjsDB.onsuccess=function(event){window.RjsTableUtils=event.target.result;var transaction=window.RjsTableUtils.transaction(["'+self.table.name+'"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] success!")};var studentsStore=transaction.objectStore("'+self.table.name+'");studentsStore.count().onsuccess=function(event){console.log("count:",event.target.result)}};')
    def reselect_table(self):
        self.table=None
    # py对象更新 db设置.重新选择表
    def set_database(self,database:RjsDatabase):
        self.database = database
        # self.reselect_table()
        #执行js代码，打开对应版本的数据库
        self.driver.execute_script('window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB'+";window.RjsDB=indexedDB.open('" + str(self.database.name) + "', "+ str(self.database.version) +");")
    def __len__(self):
        return self.driver.execute_script("return window.localStorage.length;")
    # 以map形式返回所有数据
    def items(self):
        return 1
    def keys(self):
        return 1
    def get(self, key):
        return 1
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
    def set_all(self, maps):
        for key, value in maps.items():
            self.set(key, value)
    def add(self,tableEntity):
        entityStr = self.dic2str(tableEntity)
        self.driver.execute_script('var transaction=window.RjsTableUtils.transaction(["users"],"readwrite");transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};var studentsStore=transaction.objectStore("users");studentsStore.add('+entityStr+').onsuccess=function(event){console.log("res:",event.target.result)};')

    def set(self, key, value):
        return
    def has(self, key):
        return False
    def remove(self, key):
        return 1
    def clear(self):
        return 1
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

