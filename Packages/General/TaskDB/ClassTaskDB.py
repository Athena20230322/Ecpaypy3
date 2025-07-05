import time
import LibGeneral.funcGeneral as funcGen
from  LibGeneral.SQLite3Operate import SQLiteOperate

class classTaskDB():
    def __init__(self, dbfile_path):
        self.dbfile = dbfile_path
        self.dbop = SQLiteOperate(dbfile_path)
        self._case_result_mark = None
        
        
    def createTableIfNotExt(self, tb_name, column):
        header = ','.join(column)
        is_table_exist = self.dbop.chkTableExist(tb_name)
        
        if is_table_exist is False:
            sqlstr = "CREATE TABLE %s (%s)" %(tb_name, header)
            print (sqlstr)
            self.dbop.execNonQuery(sqlstr)        
        
        
    def chkTaskTable(self):
        tasktbColumn = (
            'task_GUID TEXT PRIMARY KEY',
            'taskGenTime DATETIME DEFAULT CURRENT_TIMESTAMP',
            'taskStartTime',
            'taskExpireTime',
            'taskExpireStamp',
            'DevFrendlyName',
            'Dev_name',
            'Platform',
            'Package',
            'Test_set',
            'taskStatus',
            'TaskPID',
            'Note'
        )
        tb_name = 'tb_testTask'
        header = ','.join(tasktbColumn)
        is_task_table_exist = self.dbop.chkTableExist(tb_name)
        
        if is_task_table_exist is False:
            sqlstr = "CREATE TABLE %s (%s)" %(tb_name, header)
            print (sqlstr)
            self.dbop.execNonQuery(sqlstr)
            
    def chkCaseResultTable(self):
        result_tb_col = (
            "ID INTEGER PRIMARY KEY",
            "task_GUID TEXT",
            "CaseRuntimeUID",
            "CaseName",
            "StartTime DATETIME",
            "ExecDuration",
            "Result"
        )
        tb_name = 'tb_CaseExecResult'
        self.createTableIfNotExt(tb_name, result_tb_col)
        
    def chkCaseMsgTable(self):
        msg_tb_col = (
            'ID INTEGER PRIMARY KEY',
            'CaseRuntimeUID',
            'Msg'
        )
        tb_name = 'tb_CaseMsg'
        self.createTableIfNotExt(tb_name, msg_tb_col)
        
    def chktbWaterMark(self):
        tb_col = (
            'ID INTEGER PRIMARY KEY',
            'Name TEXT',
            'WaterMark INT DEFAULT 0',
            'LastUpdTime DATETIME DEFAULT CURRENT_TIMESTAMP'
        )
        tb_name = 'tb_TableWaterMark'
        self.createTableIfNotExt(tb_name, tb_col)    
        
    def chkCurrTaskTable(self):
        curr_task_col = (
            'ID INTEGER PRIMARY KEY',
            'task_GUID TEXT'
        )
        tb_name = 'tb_CurrentTask'
        self.createTableIfNotExt(tb_name, curr_task_col)
        
    def genCaseRuntimeRecord(self, run_guid):
        #Add record to result msg table
        stmt = """INSERT INTO tb_CaseMsg (
                                CaseRuntimeUID
                                ) 
                                VALUES (
                                '%s'
                                )""" % (run_guid)
        self.dbop.execNonQuery(stmt)
        
    
    def updateCaseExecResult(self, task_guid, run_guid, name, duration, res):
        dur_str = '-' + str(duration) + ' Second'
        start_time_cal = "(datetime(CURRENT_TIMESTAMP,'localtime', '%s'))" % (dur_str)
        stmt = """INSERT INTO tb_CaseExecResult (
                        task_GUID,
                        CaseRuntimeUID,
                        CaseName,
                        StartTime,
                        ExecDuration,
                        Result
                        ) 
                        VALUES (
                        '%s',
                        '%s',
                        '%s',
                         %s,
                        '%s',
                        '%s'
                        )""" % (task_guid, run_guid, name, start_time_cal, duration, res)
        print (stmt)
        self.dbop.execNonQuery(stmt)        

    def updateCaseMsg(self, run_uid, message):
        msg = message.replace("'", "\"")
        stmt = """UPDATE tb_CaseMsg SET 
                        Msg = '%s' 
                        WHERE
                        CaseRuntimeUID = '%s'
                        """ % (msg, run_uid)
        self.dbop.execNonQuery(stmt)
    
    def chkTaskStatus(self, task_guid):
        str_selectTaskStatus = "SELECT taskStatus FROM tb_testTask WHERE task_GUID = %s" % (task_guid)
        self.dbop.queryData(str_selectTaskStatus)
        
    def chkIfTaskRunning(self, FrendlyName, pkg, test_set):
        sqlstr_run = """SELECT task_GUID FROM tb_testTask
                            WHERE taskStatus = 'Running' 
                            AND DevFrendlyName = '%s' 
                            AND Package = '%s' 
                            AND Test_set = '%s'""" % (FrendlyName, pkg, test_set)
        guidRun = self.dbop.queryData(sqlstr_run)
        #print guidRun
        if len(guidRun) == 1:
            return True
        elif len(guidRun) == 0:
            return False
        else:
            raise ValueError("chkIfTaskRunning: Unexpected query result.")
        
    def chkIfTaskQueueing(self, FrendlyName, pkg, test_set):
        sqlstr_queue = """SELECT task_GUID FROM tb_testTask 
                            WHERE taskStatus = 'Queueing' 
                            AND DevFrendlyName = '%s' 
                            AND Package = '%s' 
                            AND Test_set = '%s'""" % (FrendlyName, pkg, test_set)
        guidQue = self.dbop.queryData(sqlstr_queue)
        if len(guidQue) == 1:
            return True
        elif len(guidQue) == 0:
            return False
        else:
            raise ValueError("chkIfTaskQueueing: Unexpected query result.")
        
    def chkTaskAval(self, FrendlyName, pkg, test_set):
        running = self.chkIfTaskRunning(FrendlyName, pkg, test_set)
        queueing = self.chkIfTaskQueueing(FrendlyName, pkg, test_set)

        
        if running is False and queueing is False:
            print ('task not exist')
            return True
        elif running is True:
            return 'Running'
        elif queueing is True:
            return 'Queueing'
        

    def isRunningWEB_Task(self):
        sqlstmt = """SELECT task_GUID FROM tb_testTask
            WHERE Platform = 'WEB' 
            AND taskStatus = 'Running'"""
        result = len(self.dbop.queryData(sqlstmt))
        if result == 0:
            return False
        elif result > 0:
            return True
        
    def addTestTask(self, info_tuple):
        add_task_stmt = """INSERT INTO tb_testTask (
                    task_GUID,
                    DevFrendlyName,
                    Platform,
                    Package,
                    Test_set,
                    taskStatus
                    ) VALUES (
                    '%s', '%s', '%s', '%s', '%s', 'Queueing'
                    )
                    """ % (info_tuple[0], info_tuple[1], info_tuple[2], info_tuple[3], info_tuple[4])

        self.dbop.execNonQuery(add_task_stmt)       
    
    def getExpiredTasks(self):
        curr_unixtime = int(time.time())
        stmt_get_exp = "SELECT task_GUID FROM tb_testTask WHERE taskStatus = 'Running' AND taskExpireStamp < %i" % (curr_unixtime)
        expired_tasks = self.dbop.queryData(stmt_get_exp)
        return expired_tasks
    
    def getRunningTasks(self):
        stmt_get_runs = "SELECT task_GUID FROM tb_testTask WHERE taskStatus = 'Running'"
        running_tasks = self.dbop.queryData(stmt_get_runs)
        return running_tasks
 
    def getQueueingTasks(self):
        stmt_get_queue = "SELECT task_GUID FROM tb_testTask WHERE taskStatus = 'Queueing'"
        queue_tasks = self.dbop.queryData(stmt_get_queue)
        return queue_tasks
    
    def getTopQueueForExec(self):
        stmt_get_queue = "SELECT task_GUID, DevFrendlyName, Package, Test_set FROM tb_testTask WHERE taskStatus = 'Queueing' LIMIT 1"
        print (stmt_get_queue)
        res = self.dbop.queryData(stmt_get_queue)
        print(("Queue for exec: %s" % (res)))
        if len(res) != 0:
            return res[0]
        else:
            return 'NoResult'
    
    def updateTaskStartTime(self, guid, expire_period=3600):
        dt = funcGen.getCurrentDatetimeStamp(mode='local')
        curr_dt = dt[0]
        curr_unix = dt[1]
        expire_unix = curr_unix + expire_period
        stmt = "UPDATE tb_testTask SET taskStartTime = '%s',taskExpireStamp = '%s'  WHERE task_GUID = '%s'" % (curr_dt, expire_unix, guid )
        
    def startTask(self, task_guid, pid):
        stmt = "UPDATE tb_testTask SET taskStatus = 'Running', TaskPID = '%s' WHERE task_GUID = '%s'" % (pid, task_guid )
        self.dbop.execNonQuery(stmt)
        stmt_add_curr = "INSERT INTO tb_CurrentTask (task_GUID) VALUES ('%s')" % (task_guid)
        print (stmt_add_curr)
        self.dbop.execNonQuery(stmt_add_curr)
        
    def setTaskComplete(self, task_guid):
        stmt = "UPDATE tb_testTask SET taskStatus = 'Complete' WHERE task_GUID = '%s'" % (task_guid)
        self.dbop.execNonQuery(stmt)
        
    def getCurrTaskStat(self):
        stmt = """SELECT 
                    T.task_GUID,
                    T.taskStatus 
                    FROM tb_testTask AS T 
                    INNER JOIN tb_CurrentTask AS CURR
                    ON T.task_GUID = CURR.task_GUID;"""
        res = self.dbop.queryData(stmt)
        return res

    def getTaskInfo(self, task_guid):
        stmt_get_info = """SELECT 
                            DevFrendlyName,
                            Dev_name,
                            Platform,
                            Package,
                            Test_set  
                            FROM tb_testTask 
                            WHERE task_GUID = '%s'""" % (task_guid)
        res = self.dbop.queryData(stmt_get_info)
        if len(res) == 1:
            return res[0]
        else:
            return False
     
       
    def getWaterMark(self, name):
        stmt = """SELECT 
                    WaterMark  
                    FROM tb_TableWaterMark 
                    WHERE Name = '%s'""" % (name)
        query = self.dbop.queryData(stmt)
        if len(query) == 0:
            return 'Not_Exist'
        else:
            return query[0][0]
        
    def setWaterMark(self, name, value):
        stmt = """UPDATE tb_TableWaterMark SET
                    WaterMark = %d
                    WHERE Name = '%s'""" % (value, name)
        query = self.dbop.execNonQuery(stmt)
        
    def createWaterMark(self, name):
        stmt = """INSERT INTO tb_TableWaterMark (
                    Name
                    ) VALUES (
                    '%s'
                    )
                    """ % (name)
        if self.getWaterMark(name) == 'Not_Exist':
            self.dbop.execNonQuery(stmt)
            
    def queryNewCaseResult(self):
        wmark = self.getWaterMark('tb_CaseExecResult')
        id_stmt = 'SELECT MAX(ID) from tb_CaseExecResult'
        query = self.dbop.queryData(id_stmt)
        if len(query) == 0:
            latest_id = 0
        else:
            latest_id = query[0][0]
        if latest_id == wmark:
            return 'No_Update'
        elif latest_id > wmark:
            stmt_gen_tmp = """
                            CREATE TABLE tb_CaseExecResult_tmp (
                                ID INTEGER PRIMARY KEY,
                                task_GUID TEXT,
                                CaseRuntimeUID,
                                CaseName,
                                StartTime DATETIME,
                                ExecDuration,
                                Result
                                );
                                        
                            INSERT INTO tb_CaseExecResult_tmp
                                SELECT
                                ID,
                                task_GUID,
                                CaseRuntimeUID,
                                CaseName,
                                StartTime,
                                ExecDuration,
                                Result
                                FROM tb_CaseExecResult WHERE ID > %d;

                        """ % (wmark)
            
            stmt_get_res = """SELECT 
                                RE.task_GUID,
                                RE.CaseRuntimeUID,
                                RE.CaseName,
                                RE.StartTime,
                                RE.ExecDuration,
                                RE.Result,
                                M.Msg
                                FROM tb_CaseExecResult_tmp AS RE
                                inner join 
                                tb_CaseMsg AS M 
                                ON RE.CaseRuntimeUID =  M.CaseRuntimeUID;
                                """
            stmt_drop_tmp = "DROP TABLE tb_CaseExecResult_tmp;"
            gen_tmp = self.dbop.execScript(stmt_gen_tmp)
            get_res = self.dbop.queryData(stmt_get_res)
            droptb = self.dbop.execNonQuery(stmt_drop_tmp)
            self._case_result_mark = latest_id
            return get_res
        
    def monCompleteTask(self):
        #inner join curr task & task stat, filter those completed
        pass
    
    def getCurrTaskSummary(self):
        stat_sum_data = """
                    CREATE TABLE tb_taskStat_tmp (
                        ID INTEGER PRIMARY KEY,
                        Guid TEXT,
                        RtnCode integer,
                        Result_txt TEXT);
                    
                    INSERT INTO tb_taskStat_tmp
                        SELECT 
                        RE.ID,
                        RE.task_GUID,
                        RE.Result,
                        CASE
                            WHEN [Result] = '100' THEN 'Pass' else 'Fail'
                        END as Result_txt
                        from tb_CaseExecResult AS RE
                        INNER JOIN tb_CurrentTask AS CURR
                        ON RE.task_GUID = CURR.task_GUID;
                    """
        stat_summ = """
                    SELECT Guid, Result_txt, count(Guid) AS Count FROM tb_taskStat_tmp GROUP BY Guid, Result_txt; 
                    """
        stmt_drop_tmp = "DROP TABLE tb_taskStat_tmp;"
        #droptb = self.dbop.execNonQuery(stmt_drop_tmp)
        gen_data = self.dbop.execScript(stat_sum_data)
        get_res = self.dbop.queryData(stat_summ)
        droptb = self.dbop.execNonQuery(stmt_drop_tmp)
        return get_res

    def rmCompleteCurrTask(self, guids):
        if type(guids) is list and len(guids) > 0:
            for uid in guids:
                stmt = "DELETE FROM tb_CurrentTask WHERE task_GUID = '%s'" % (uid)
                self.dbop.execNonQuery(stmt)


    #def queryExpiredTask():
        
    #def queryTaskPID(self, guid):
    
