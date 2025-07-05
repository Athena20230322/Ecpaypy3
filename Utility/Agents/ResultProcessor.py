import LibGeneral.funcGeneral as funcGen
import TaskDB.ClassTaskDB as TDB
import LibGeneral.GetConfigValue as getConf
import os
import time
from LibGeneral.AddLog import customLog
from TestCenterDB.CenterDB import clsTestCenterDB


def cleanup():
    print('CLEANUP!!!!')
    os.remove(TERM_FLAG)
    sys.exit(0)


PJOIN = os.path.join

CONF = getConf.getConfig()
ROOTDIR = CONF.getRootDir()       
taskDB = PJOIN(ROOTDIR, 'Utility', 'DB', 'TestTaskDB.db')
TESTDB = TDB.classTaskDB(taskDB)
CENTERDB = clsTestCenterDB()


f = 1
TERM_FLAG = PJOIN(ROOTDIR, 'Tmp', 'TermResultProcessor')

while f == 1:
    
    if os.path.exists(TERM_FLAG):
        cleanup()

    else:
        CURR_TASK_STAT = TESTDB.getCurrTaskStat()
        TESTDB.chktbWaterMark()
        TESTDB.createWaterMark('tb_CaseExecResult')
        NEW_RESULT = TESTDB.queryNewCaseResult()
        TASKS_SUMM = TESTDB.getCurrTaskSummary()
        COMP_TASK = [x[0] for x in CURR_TASK_STAT if x[1] == 'Complete']
        if len(CURR_TASK_STAT) > 0:
            #try:
            CENTERDB.insertNewCaseResult(NEW_RESULT)
            CENTERDB.updateTaskSumm(TASKS_SUMM)
            #except:
                #print "Exception occurs"        
            #else:
            if TESTDB._case_result_mark is not None:
                TESTDB.setWaterMark('tb_CaseExecResult', TESTDB._case_result_mark)
                #try:
                CENTERDB.updateTaskStat(CURR_TASK_STAT)
                #else:
                TESTDB.rmCompleteCurrTask(COMP_TASK)
        

            
    time.sleep(10)

