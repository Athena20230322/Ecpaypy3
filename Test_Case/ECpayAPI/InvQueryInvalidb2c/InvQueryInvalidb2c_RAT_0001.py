# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvIssueb2c import actInvIssueb2c
from ECpay.ProdActions.ActECpayAPI.ActInvIssueInvalidb2c import actInvIssueInvalidb2c
from ECpay.ProdActions.ActECpayAPI.ActInvQueryInvalidb2c import actInvQueryInvalidb2c
from ECpay.Verification.VerifyECpayAPI.VerifyInvQueryInvalidb2c import verifyInvQueryInvalidb2c


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
INVALID_API = actInvIssueInvalidb2c()
ACT_API = actInvQueryInvalidb2c()
VER_API = verifyInvQueryInvalidb2c()

# Testing exec
# precondition-InvIssue
ISSUE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryInvalidb2c', 'Initial_Data', 'InvIssue.csv')


issue_info = EXEC_ACT(ISSUE_API.genOrderRequestInfoB2c, ISSUE_INFO_CSV)

data1 = EXEC_ACT(ISSUE_API.decryptDatab2c,issue_info['Data'])

issue_rtn = EXEC_ACT(ISSUE_API.genPostRequestToAPI, issue_info)


res_dict1 = EXEC_ACT(ISSUE_API.strToDict, issue_rtn)

data2 = EXEC_ACT(ISSUE_API.decryptDatab2c, res_dict1['Data'])
print(data2)


# precondition-InvIssueInvalid
INVALID_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryInvalidb2c', 'Initial_Data', 'InvIssueInvalid.csv')

invalid_info = EXEC_ACT(INVALID_API.genOrderRequestInfoB2c, INVALID_INFO_CSV, data2,data1)

#invalid_info = EXEC_ACT(INVALID_API.genOrderRequestInfoB2c, INVALID_INFO_CSV, invalid_revert, data1)

api_response = EXEC_ACT(INVALID_API.genpostRequestToAPI, invalid_info,
                       'https://einvoice-stage.ecpay.com.tw/B2CInvoice/Invalid')

#api_response = EXEC_ACT(INVALID_API.genPostRequestToAPIb, invalid_info)

res_dict = EXEC_ACT(INVALID_API.strToDict, api_response)

data3 = EXEC_ACT(INVALID_API.decryptDatab2c, res_dict['Data'])
print(data3)


# InvQueryInvalid
QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryInvalidb2c', CASE_NAME, 'InvQueryInvalid.csv')

query_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2cS, QUERY_INFO_CSV, data1,data2)

api_response = EXEC_ACT(ACT_API.genPostRequestToAPIb2c, query_info)

res_dict = EXEC_ACT(ACT_API.strToDict, api_response)

# verification
#VERIFY(VER_API.verifyResponseValue, query_rtn_dict, issue_info, issue_rtn_dict, invalid_info, CASE_NAME)

data = EXEC_ACT(ACT_API.decryptDatab2c2, res_dict['Data'])
# verification
#VERIFY(VER_API.verifyResponseValueb2c, data,data1,data2,data3,CASE_NAME)

#VERIFY(VER_API.verifyResponseValueb2c, CASE_NAME, data)

VERIFY(VER_API.verifyColumn,  data,CASE_NAME)

time.sleep(5)

HELPER.processResult(caserun_uid=RUN_UID)