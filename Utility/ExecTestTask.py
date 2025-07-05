import datetime
import os
import re
import sys
import argparse
import PyDataSet.pyDataSet
import LibGeneral.funcGeneral as funcGen
import TaskDB.ClassTaskDB as TDB
import LibGeneral.GetConfigValue as getConf
import subprocess
import time
from LibGeneral.AddLog import customLog
from TestCenterDB.CenterDB import clsTestCenterDB


PJOIN = os.path.join
CONF = getConf.getConfig()
ROOTDIR = CONF.getRootDir() 
LOG_FOLDER = PJOIN(ROOTDIR, 'Logs')

taskDB = PJOIN(ROOTDIR, 'Utility', 'DB', 'TestTaskDB.db')
PYDS = PyDataSet.pyDataSet.classPyDataSet()
CLS_TDB = TDB.classTaskDB(taskDB)
CENTERDB = clsTestCenterDB()

PROC = subprocess

argp = argparse.ArgumentParser(description='Script for parallel executing test task.')
argp.add_argument('--guid' , type = str, default='', help = 'Specify the task guid for retrieving related info from local test DB. If this option is specified, others would be overwritten')
argp.add_argument('--dev' , type = str, default='', help = 'Specify the frendly name of test device.')
argp.add_argument('--pkg' , type = str, help = 'Specify the frendly name of package to test.')
argp.add_argument('--testset' , type = str, help = 'Specify the name of test set.')
args = argp.parse_args()

t_guid = args.guid

DevListFile = PJOIN(ROOTDIR, 'Conf', 'DeviceList.csv')
DevList = PYDS.importCSV(DevListFile)

if t_guid is None or t_guid == '':
    #t_guid = 'empty_guid'
    t_guid = funcGen.genRandomUuid(with_dash=False)
    test_set = args.testset
    dev_name = args.dev
    package = args.pkg
    if dev_name:
        DevInfo = PYDS.queryDataSet(DevList, ["Device_Name", "Platform", "OS_Version"], criteria=["Device_Frendly_Name = '%s'" % (dev_name)], withHeader=False, expResCnt=1)
        dev_real_id = DevInfo[0][0]
        dev_platform = DevInfo[0][1]
        dev_os_ver = DevInfo[0][2]
    else:
        dev_real_id = 'NotSecified'
        dev_platform = 'NotSecified'
        dev_os_ver = 'NotFound'
    
elif len(t_guid) == 32:
    task_info = CLS_TDB.getTaskInfo(t_guid)
    print("TASK_INFO:" , task_info)
    dev_name = task_info[0]
    dev_real_id = task_info[1]
    dev_platform = task_info[2]
    package = task_info[3]
    test_set = task_info[4]
    DevInfo = PYDS.queryDataSet(DevList, ["Platform", "OS_Version"], criteria=["Device_Frendly_Name = '%s'" % (dev_name)], withHeader=False, expResCnt=1)
    dev_os_ver = DevInfo[0][1]

if dev_name:    
    print(dev_real_id)
    print("PLATFORM", dev_platform)
    print(dev_os_ver)

TIMESTMP = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
LOG_DIR = '_'.join(['Log_', test_set, TIMESTMP])
LOG_FILE = '_'.join(['TaskLog', t_guid]) + '.log'
LOG = customLog()
LOG.createLogger(PJOIN(LOG_DIR, LOG_FILE))


tspath = PJOIN(ROOTDIR, 'Test_Set', test_set) + r'.txt'
with open(tspath, 'r') as cases:
    t_set_content = cases.readlines()
    print(t_set_content)

case_re_ptn = "_\d{4}.py"
match_lines = []
for line in t_set_content:
    hit = re.search(case_re_ptn, line)
    
    if hit is not None:
        print("Line contains test case:", hit.string)
        match_lines.append(line) 
        
cases_cnt = len(match_lines)
time.sleep(3)
try:
    CENTERDB.startTask(t_guid, cases_cnt, datetime.datetime.strptime(TIMESTMP, '%Y-%m-%d_%H_%M_%S'))
except Exception as err:
    err_msg = err.message
    LOG.ERROR(err_msg)
else:
    msg = "Start task (uid: %s), case count: %i" % (t_guid, cases_cnt)
    LOG.INFO(msg)
    
#update task info
for case in match_lines:
    print("case: %s" % case)
    case = case.strip('\n')
    case_path = PJOIN(ROOTDIR, 'Test_Case', case)
    runtime_uid = str(funcGen.genRandomUuid())
    case_name = os.path.basename(case_path).strip('.py')
    CLS_TDB.genCaseRuntimeRecord(runtime_uid)
    time_start = time.time()
    if dev_platform == 'Web':
        print(case_path)
        ret = PROC.Popen(['python.exe', case_path, '--logdir', LOG_DIR, '--package', package, '--runid', runtime_uid], shell=False).wait()
    elif dev_platform == 'API':
        print(case_path)
        ret = PROC.Popen(['python.exe', case_path, '--logdir', LOG_DIR, '--package', package, '--runid', runtime_uid], shell=False).wait()
    else:
        ret = PROC.Popen(['python.exe', case_path, '--logdir', LOG_DIR, '--package', package, '--runid', runtime_uid], shell=False).wait()
        
    print("return code : " , ret)
    if ret == 100:
        case_result = 'PASS'
    elif ret == 103:
        case_result = 'FAIL'
    elif ret == 2:
        case_result = 'Case File Not Found'
    elif ret == 1:
        case_result = 'Error interupt during case exec'
    else:
        case_result = 'Unknown case return code'
    time_comp = time.time()
    exec_dur = "{0:.3f}".format(time_comp - time_start)
    
    print("EXEC Duration :", exec_dur)
    CLS_TDB.updateCaseExecResult(t_guid, runtime_uid, case_name, exec_dur, ret)
    LOG.INFO("Execute test case %r, return code : %s" % (case, case_result))


time.sleep(10)
CLS_TDB.setTaskComplete(t_guid)