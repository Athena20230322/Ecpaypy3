# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvIssueb2c import actInvIssueb2c
from ECpay.ProdActions.ActECpayAPI.ActInvQueryb2c import actInvQueryb2c
from ECpay.Verification.VerifyECpayAPI.VerifyInvQueryb2c import verifyInvQueryb2c


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
ISSUE_API = actInvIssueb2c()
ACT_API = actInvQueryb2c()
VER_API = verifyInvQueryb2c()

# Testing exec
# precondition-InvIssue
INV_ISSUE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryb2c', 'Initial_Data', 'InvIssue.csv')

inv_info = EXEC_ACT(ISSUE_API.genOrderRequestInfoB2c, INV_ISSUE_INFO_CSV)

data1=EXEC_ACT(ISSUE_API.decryptDatab2c, inv_info['Data'])

invoice_rtn = EXEC_ACT(ISSUE_API.genPostRequestToAPI, inv_info)

res_dict = EXEC_ACT(ISSUE_API.strToDict, invoice_rtn)

data = EXEC_ACT(ISSUE_API.decryptDatab2c, res_dict['Data'])
print(data)

# InvQuery
QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryb2c', CASE_NAME, 'Query.csv')

query_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2cS, QUERY_INFO_CSV, data1,data)

query_rtn = EXEC_ACT(ACT_API.genPostRequestToAPI, query_info)

query_rtn_dict = EXEC_ACT(ACT_API.strToDict, query_rtn)

data = EXEC_ACT(ACT_API.decryptDatab2c2, query_rtn_dict['Data'])
print(data)

# verification
VERIFY(VER_API.verifyColumn, CASE_NAME, data)
time.sleep(3)
# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
