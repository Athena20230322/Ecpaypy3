import sqlite3

class SQLiteOperate():
    def __init__(self, DBfilePath):
        self.con = sqlite3.connect(DBfilePath)
        self.cur = self.con.cursor()
    
    def queryData(self, statement):
        self.cur.execute(statement)
        result = self.cur.fetchall()
        return result
        
        
    def execNonQuery(self, statement):
        self.cur.execute(statement)
        self.con.commit()
        
    def execScript(self, sc):
        self.cur.executescript(sc)
        
        
    def chkTableExist(self, tbname):
        query = "SELECT count(name) FROM sqlite_master WHERE type = 'table' and name = '%s'" % (tbname)
        self.cur.execute(query)
        qraw = self.cur.fetchall()
        qresult = qraw[0][0]
        print (qresult)
        if qresult == 0:
            return False
        elif qresult ==1:
            return True
        else:
            error_msg = "chkTableExist : The query result is not expected. Result should be 0 or 1. Current value = %s" % (qresult)
            raise ValueError(error_msg)
        
        
        
        
        
        