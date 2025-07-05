# -*- coding: utf-8 -*-
import MySQLdb

class MariaOperate():
    def __init__(self, dbhost, default_db, usr, pwd):
        self.dhost = dbhost
        self.defdb = default_db
        self.dbusr = usr
        self.dbpwd = pwd
        
        
    def newConn(self):
        con = MySQLdb.connect(host=self.dhost, db=self.defdb, user=self.dbusr, passwd=self.dbpwd, charset='utf8')
        return con

    
    def queryData(self, statement):
        conn = self.newConn()
        cur = conn.cursor()
        cur.execute(statement)
        result = cur.fetchall()
        conn.close()
        return result
        
        
    def execNonQuery(self, statement):
        conn = self.newConn()
        cur = conn.cursor()        
        cur.execute(statement)
        conn.commit()
        conn.close()
        return True
        
    #def chkTableExist(self, tbname):
        #querystr = "SELECT count(name) FROM sqlite_master WHERE type = 'table' and name = '%s'" % (tbname)
        #self.cur.execute(querystr)
        #qraw = self.cur.fetchall()
        #qresult = qraw[0][0]
        #print qresult
        #if qresult == 0:
            #return False
        #elif qresult ==1:
            #return True
        #else:
            #error_msg = "chkTableExist : The query result is not expected. Result should be 0 or 1. Current value = %s" % (qresult)
            #raise ValueError(error_msg)
            
#maria = MariaOperate('104.214.145.51', 'test', 'testing_usr', '1qaz@WSX3306')
#MANAGED_DB = maria.queryData('SHOW DATABASES;')
#print MANAGED_DB
