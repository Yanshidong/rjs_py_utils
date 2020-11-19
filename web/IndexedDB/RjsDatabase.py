
class RjsDatabase:

    def setDbName(self,name):
        self.name=name
    def getDbName(self):
        return self.name
    def setDbVersion(self,version):
        self.version=version
    def getDbVersion(self):
        return self.version

    def __init__(self,name,version=1) -> None:
        self.setDbName(name)
        self.setDbVersion(version)
