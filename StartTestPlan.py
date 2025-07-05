import argparse
import datetime
import os
import requests
import urllib.parse
import LibGeneral.funcGeneral as funcGen
from TestCenterDB.CenterDB import clsTestCenterDB
import PyDataSet.pyDataSet

PJOIN = os.path.join
URLJOIN = urllib.parse.urljoin
ROOTDIR = os.path.dirname(os.path.realpath(__file__))
LOGFOLDER = PJOIN(ROOTDIR, 'Logs')
TASKEXECUTOR = PJOIN(ROOTDIR, 'Utility', 'ExecTestTask.py')
DEVLISTFILE = PJOIN(ROOTDIR, 'Conf', 'DeviceList.csv')
PY_DS = PyDataSet.pyDataSet.classPyDataSet()
GEN_GUID = funcGen.genRandomUuid

CENTERDB = clsTestCenterDB()

ARG_PARSE = argparse.ArgumentParser(description='Script for executing test plan.')
ARG_PARSE.add_argument('-p', type=str, help='Specifiy test plan CSV file for a test scenario, usually these files would be in Plan folder.')
ARG_PARSE.add_argument('-n', type=str, default='', help='Specifiy test plan runtime name. You might specify an empty string to use the file name and current time for naming')
ARGS = ARG_PARSE.parse_args()
PLAN_FILE = ARGS.p
RUN_NAME = ARGS.n
PLAN_NAME = os.path.basename(PLAN_FILE).strip('.csv')
PLAN_GUID = funcGen.genRandomUuid()
    
if RUN_NAME == '':
    TIMESTMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    RUN_NAME = PLAN_NAME + TIMESTMP

if PLAN_FILE:
    planFileDefaultPath = PJOIN(ROOTDIR, 'Plan', PLAN_FILE)
    if os.path.exists(PLAN_FILE) or os.path.exists(planFileDefaultPath):
        TASK_GEN_TIME = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        print(TASK_GEN_TIME)
        test_plan = PY_DS.importCSV(PLAN_FILE)
        PY_DS.printDataSet(test_plan)
        TASKS = PY_DS.queryDataSet(test_plan, ('Device', 'Package', 'TestSet'), withHeader=False)
        devList = PY_DS.importCSV(DEVLISTFILE)
        tasks_info = []
        for row in TASKS:
            print(row)
            task_GUID = GEN_GUID(False)
            print(task_GUID)
            devName = row[0]
            pkgName = row[1]
            testSetName = row[2]
            criGetDevHost = "Device_Frendly_Name = '%s'" % (devName)
            task_name = testSetName
            print(type(criGetDevHost))
            devHost = PY_DS.queryDataSet(devList, ('Device_Host',), criteria=(criGetDevHost,), withHeader=False)
            print(devHost[0][0])
            newTaskJSON = {
                "DevFrendName": devName, 
                "GUID": task_GUID, 
                "Package": pkgName, 
                "Test_set": testSetName
            }               
            print(pkgName)
            print(testSetName)
            reqHostURL = ''.join(('http://', devHost[0][0], ':8000'))
            print(reqHostURL)
            req = requests.post(reqHostURL, json=newTaskJSON)
            tinfo = (str(PLAN_GUID), task_GUID, str(task_name))
            tasks_info.append(tinfo)
            print(tasks_info)
            #os.system("%s --dev %s --pkg %s --set %s" % (taskExecutor, devName, pkgName, testSetName )) 
        
        TASK_COUNT = len(tasks_info)
        CENTERDB.addRunningPlan(PLAN_GUID, RUN_NAME, PLAN_NAME, TASK_COUNT)
        CENTERDB.addTestTasks(tasks_info)
        
    else:
        print("Error : Specified task file not found.")

else:
    print("Error : Plan file name cannot be empty.")

#logFile = "_".join([TASK_GEN_TIME, task_GUID])
