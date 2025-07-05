# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvDelayb2c import actInvDelayb2c
from ECpay.ProdActions.ActECpayAPI.ActInvTriggerb2c import actInvTriggerb2c
from ECpay.Verification.VerifyECpayAPI.VerifyInvTriggerb2c import verifyInvTriggerb2c


#(DO NO Edit) Static declare

ARGP = argparse.ArgumentParser(description='Script for exec test.')
ARGP.add_argument('--logdir', type=str, help='Specify the log dir')
ARGP.add_argument('--package', type=str, help='Specify the package name')
ARGP.add_argument('--runid', type=str, default='', help='Specify the runtime guid for this run.')
ARGS = ARGP.parse_args()
LOG_DIR = ARGS.logdir
PKG = ARGS.package
RUN_UID = ARGS.runid
CASE_NAME = str(os.path.basename(__file__)).rstrip('.py')
SUM_LOG = os.path.join(LOG_DIR, CASE_NAME, 'Summary.log')
HELPER = classTestHelper(SUM_LOG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
DELAY_API = actInvDelayb2c()
ACT_API = actInvTriggerb2c()
VER_API = verifyInvTriggerb2c()

# Testing exec
# precondition-InvDelay
DELAY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvTriggerb2c', 'Initial_Data', 'InvDelay.csv')


delay_issue_info = EXEC_ACT(DELAY_API.genOrderRequestInfoB2citem, DELAY_INFO_CSV)

data2 = EXEC_ACT(ACT_API.decryptDatab2c, delay_issue_info['Data'])

delay_rtn = EXEC_ACT(DELAY_API.genPostRequestToAPI, delay_issue_info,)

res_dict = EXEC_ACT(ACT_API.strToDict, delay_rtn)

data = EXEC_ACT(ACT_API.decryptDatab2c2, res_dict['Data'])
print(data)

# InvTrigger
delay_rtn_dict = EXEC_ACT(ACT_API.strToDict, delay_rtn)

data = EXEC_ACT(ACT_API.decryptDatab2c2, delay_rtn_dict['Data'])

TRIGGER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvTriggerb2c', CASE_NAME, 'InvTrigger.csv')

trigger_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2c, TRIGGER_INFO_CSV, data2)

trigger_rtn = EXEC_ACT(ACT_API.genPostRequestToAPI, trigger_info)

trigger_rtn_dict = EXEC_ACT(ACT_API.strToDict, trigger_rtn)

data1 = EXEC_ACT(ACT_API.decryptDatab2c2, trigger_rtn_dict['Data'])
print(data1)

# verification
VERIFY(VER_API.verifyInjection, data1, data, CASE_NAME)



# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
