# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvWordSettingb2c import actInvWordSettingb2c
from ECpay.Verification.VerifyECpayAPI.VerifyInvWordSettingb2c import verifyInvWordSettingb2c


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
ACT_API = actInvWordSettingb2c()
VER_API = verifyInvWordSettingb2c()

# Testing exec

# InvQuery
QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvWordSettingb2c', CASE_NAME, 'Query.csv')

query_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2cSWordSetting, QUERY_INFO_CSV)

query_rtn = EXEC_ACT(ACT_API.genPostRequestToAPIWordSetting, query_info)

query_rtn_dict = EXEC_ACT(ACT_API.strToDict, query_rtn)

data = EXEC_ACT(ACT_API.decryptDatab2c2, query_rtn_dict['Data'])
print(data)

# verification
VERIFY(VER_API.verifyResponseValueb2c, CASE_NAME, data)
time.sleep(3)
# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
