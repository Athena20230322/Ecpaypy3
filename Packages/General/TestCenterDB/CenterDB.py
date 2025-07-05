
import LibGeneral.GetConfigValue as getConf
from LibGeneral.SQLServerOperate import MSSQL
import time

class clsTestCenterDB():
    def __init__(self):
        general_conf = getConf.getConfig()
        self.dbsetting = general_conf.getCenterDBSetting() 
        self.task_tb = '.'.join([self.dbsetting['dbn'], '[dbo]', '[tb_TaskStat]'])
        self.casestat_tb = '.'.join([self.dbsetting['dbn'], '[dbo]', '[tb_CaseStat]'])

        if self.dbsetting['is_enable'] == 'True':
            self.cdb = MSSQL(self.dbsetting['hoststr'], self.dbsetting['dbn'], self.dbsetting['user'], self.dbsetting['pwd'])
            self.is_enabled = True
        else:
            self.is_enabled = False
            print("Use TestCenterDB is disabled.") 
            
    @property
    def isEnabled(self):
        return self.is_enabled
    

    def enableLog(self, logobj):
        self._log = logobj
    
    def addRunningPlan(self, plan_uid, runtime_name, plan_name, case_amt):
        if self.is_enabled == True:
            plan_stmt = """INSERT INTO [dbo].[tb_TestPlanStat] (
                            PlanRuntimeGUID,
                            RuntimeName,
                            Filename,
                            TaskAmount
                            ) VALUES(
                            %s,
                            %s,
                            %s,
                            %d
                            )""",  (plan_uid, runtime_name, plan_name, case_amt)
            self.cdb.execNonQuery(plan_stmt)
        else:
            print("Use TestCenterDB is disabled.")
    
    def addTestTasks(self, tasks_info):
        if self.is_enabled == True:
            self.cdb.InsertMany(self.task_tb,
            ('PlanRuntimeGUID', 'TaskGUID', 'TaskName'),
            tasks_info)            
        else:
            print("Use TestCenterDB is disabled.")
    
    def startTask(self, task_guid, case_amt, time_stamp):
        #update start time, case amount
        if self.is_enabled == True:
            stmt = """UPDATE [dbo].[tb_TaskStat] SET 
                        [StartTime] = %s, 
                        [SumCaseAmount] = %d 
                        WHERE 
                        [TaskGUID] = %s
                            """, (time_stamp, case_amt, task_guid)
            stmt_q = """SELECT TaskGUID FROM [dbo].[tb_TaskStat] WITH (NOLOCK)
                        WHERE 
                        [TaskGUID] = %s
                            """, (task_guid)            
            try:
                rec_exist = self.cdb.safeQueryData(stmt_q)
                while rec_exist == []:
                    time.sleep(2)
                    rec_exist = self.cdb.safeQueryData(stmt_q)
                self.cdb.execNonQuery(stmt)
            except Exception:
                time.sleep(1)
                self.cdb.execNonQuery(stmt)
            else:
                print("Task %s info updated" % (task_guid))
            #finally:
                #time.sleep(3)
                #still_null = self.cdb.safeQueryData(stmt_q)
                #if still_null:
                    #self.cdb.execNonQuery(stmt)
            
        else:
            print("Use TestCenterDB is disabled.")
    
    def updateTaskSumm(self, data):
        #pass, fail, lastupdate time
        for row in data:
            task_guid = row[0]
            case_stat = row[1]
            cnt = int(row[2])
            if case_stat == 'Pass':
                stmt = "UPDATE [dbo].[tb_TaskStat] SET [LastUpdTime] = GETDATE(), [PassAmt] = %d WHERE [TaskGUID] = %s", (cnt, task_guid)
            elif case_stat == 'Fail':
                stmt = "UPDATE [dbo].[tb_TaskStat] SET [LastUpdTime] = GETDATE(), [FailAmt] = %d WHERE [TaskGUID] = %s", (cnt, task_guid)
            else:
                print("updateTaskStat: Status of task [%s] is unexpected." % (task_guid))
            self.cdb.execNonQuery(stmt)
        
        return True
    
    def updateTaskStat(self, data):
        #update stat
        for row in data:
            task_guid = row[0]
            stat = row[1]
            stmt = "UPDATE [dbo].[tb_TaskStat] SET [Status] = %s WHERE [TaskGUID] = %s" , (stat, task_guid)
            self.cdb.execNonQuery(stmt)
    
    def insertNewCaseResult(self, data):
        if self.is_enabled == True:
            if data is None or len(data) == 0:
                print("No result need to be updated")
            else:
                self.cdb.InsertMany(self.casestat_tb,
                ('TaskGUID', 'CaseRuntimeGUID', 'CaseID', 'StartTime', 'ExecDuration', 'Status', 'ExecMsg'),
                data)            
        else:
            print("Use TestCenterDB is disabled.")
        
        

class scheduleTask():
    def __init__(self):
        general_conf = getConf.getConfig()
        self.dbsetting = general_conf.getCenterDBSetting() 
        self.task_tb = '.'.join([self.dbsetting['dbn'], '[dbo]', '[tb_TaskStat]'])
        self.casestat_tb = '.'.join([self.dbsetting['dbn'], '[dbo]', '[tb_CaseStat]'])

        if self.dbsetting['is_enable'] == 'True':
            self.cdb = MSSQL(self.dbsetting['hoststr'], self.dbsetting['dbn'], self.dbsetting['user'], self.dbsetting['pwd'])
            self.is_enabled = True
        else:
            self.is_enabled = False
            print("Use TestCenterDB is disabled.") 
            
    def ExecScheduleJob(self):
        stmt = "EXEC [dbo].[sp_ExecScheduleTask]", ()
        self.cdb.execNonQuery(stmt)