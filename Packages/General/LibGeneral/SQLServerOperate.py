# -*- coding: utf-8 -*-

import pymssql
import LibGeneral.funcGeneral as funcGen

class MSSQL():
    def __init__(self, dbhost, default_db, usr, pwd):
        self.dhost = dbhost
        self.defdb = default_db
        self.dbusr = usr
        self.dbpwd = pwd
        
        
    def newConn(self):
        con = pymssql.connect(self.dhost, self.dbusr, self.dbpwd, self.defdb)
        return con

    
    def queryData(self, statement):
        conn = self.newConn()
        cur = conn.cursor()
        cur.execute(statement)
        result = cur.fetchall()
        conn.close()
        return result
        
    def safeQueryData(self, statement):
        conn = self.newConn()
        cur = conn.cursor()
        cur.execute(statement[0], statement[1])
        result = cur.fetchall()
        conn.close()
        return result    
        
    def execNonQuery(self, statement):
        conn = self.newConn()
        cur = conn.cursor()        
        cur.execute(statement[0], statement[1])
        conn.commit()
        conn.close()
        return True
    
    def InsertMany(self, db, col, val):
        if type(col) is tuple:
            if type(val) is tuple or type(val) is list:
                column_str = col.__str__().replace("'", "")
                val_modstr = funcGen.listToModuloStr(val[0])
                stmt = "INSERT INTO [DBN] [COLUMN] VALUES [VAL]"
                label_corr = {
                            '[DBN]' : db,
                            '[COLUMN]' : column_str,
                            '[VAL]' : val_modstr
                            }
                for k in list(label_corr.keys()):
                    stmt = stmt.replace(k, label_corr[k])
                print(stmt)
                conn = self.newConn()
                cur = conn.cursor()
                try:
                    cur.executemany(stmt, val)
                except Exception as err:
                    conn.close()
                    print("Exception occurs when execute insertMany method, Error: %s" % (err))
                    raise pymssql.DatabaseError("Exception occurs when execute insertMany method, Error: %s" % (err))
                else:
                    conn.commit()
                    conn.close()
                finally:
                    pass
            elif val == 'No_Update':
                print("InsertMany: No data for processing...")
            else:
                raise TypeError("MSSQL.InsertMany : Recieved parameter 'val' is not a tuple or list.")
        else:
            raise TypeError("MSSQL.InsertMany : Recieved parameter 'col' is not a tuple.")
        
    def UpdateMany(self, db, col, val):
        pass
        
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
