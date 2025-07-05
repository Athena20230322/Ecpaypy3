import os
import sys
import time
import datetime
import sqlite3
import TaskDB.ClassTaskDB as TDB
import LibGeneral.GetConfigValue as getConf
import subprocess
from LibGeneral.SQLServerOperate import MSSQL

def cleanup():
    print('CLEANUP!!!!')
    os.remove(TERM_FLAG)
    sys.exit(0)


PJOIN = os.path.join

CONF = getConf.getConfig()
ROOTDIR = CONF.getRootDir()       
taskDB = PJOIN(ROOTDIR, 'Utility', 'DB', 'TestTaskDB.db')
PROC = subprocess

GEN_CONF = getConf.getConfig()


'''
. Stop expired task
. Count current running task 
. If there's Web testing proceeding, not start new task on this machine
. if running task less than 5, query if there's any task queueing.
. If there's new task queueing, start it through task Executor on new console, retrieve its PID & update it into DB
. update local sqlite , add task start time,  expire time and stamp


. monitor task status
. send test result to result DB
. purge timeout task
. purge timeout dataset db file


'''

f = 1
TERM_FLAG = PJOIN(ROOTDIR, 'Tmp', 'TermTaskProcessor')

while f == 1:
    
    if os.path.exists(TERM_FLAG):
        cleanup()

    else:
        CLSTDB = TDB.classTaskDB(taskDB)
        CLSTDB.chkTaskTable() 
        CLSTDB.chkCurrTaskTable()
        CLSTDB.chkCaseResultTable()
        CLSTDB.chktbWaterMark()
        CLSTDB.chkCaseMsgTable()
        TaskExpire = CLSTDB.getExpiredTasks()
        lenExpTask = len(TaskExpire)
        
        if lenExpTask > 0:
            print("Stop expired task")
            for task in TaskExpire:
                print("stop expired task , GUID : %s" % (task))
                #Get PID and kill it
                
        
        IS_WEB_RUN = CLSTDB.isRunningWEB_Task()
        if IS_WEB_RUN is True:
            print('There is running WEB testing on this machine, exit.')
        elif IS_WEB_RUN is False:
            
            
            LEN_RUN_TASK = len(CLSTDB.getRunningTasks())
            if LEN_RUN_TASK < 5:
                print('start a new task')
                executor = PJOIN(ROOTDIR, 'Utility', 'ExecTestTask.py')
                taskinfo = CLSTDB.getTopQueueForExec()
                if taskinfo != 'NoResult':
                    print("task info:" ,taskinfo)
                    
                    task_guid = taskinfo[0]
                    dev_frend_name = taskinfo[1]
                    package = taskinfo[2]
                    t_set = taskinfo[3]
                    
                    cmd = "%s --dev '%s' --pkg '%s' --testset '%s'" % (executor, dev_frend_name, package, t_set)
                    print(cmd)
                    #task = PROC.Popen(['python.exe', executor, '--dev' ,dev_frend_name, '--pkg', package, '--testset', t_set], shell=False  )
                    task = PROC.Popen(['python.exe', executor, '--guid', task_guid], shell=False )
                    print(task.pid)
                    CLSTDB.startTask(task_guid, task.pid)


        print('processed')
        time.sleep(5)
        



