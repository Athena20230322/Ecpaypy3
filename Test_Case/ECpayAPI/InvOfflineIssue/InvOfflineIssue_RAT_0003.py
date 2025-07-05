# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os


#Feature related test package import

from ECpay.ProdActions.ActECpayAPI.ActInvOfflineGetInvoiceWordSetting import actInvOfflineGetInvoiceWordSetting
from ECpay.Verification.VerifyECpayAPI.VerifyInvOfflineGetInvoiceWordSetting import verifyInvOfflineGetInvoiceWordSetting

from ECpay.ProdActions.ActECpayAPI.ActInvOfflineIssue import actInvOfflineIssue
from ECpay.Verification.VerifyECpayAPI.VerifyInvOfflineIssue import verifyInvOfflineIssue


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

ACT_API = actInvOfflineGetInvoiceWordSetting()
VER_API = verifyInvOfflineGetInvoiceWordSetting()

ACT_API1 = actInvOfflineIssue()
VER_API1 = verifyInvOfflineIssue()

# Testing exec

# InvQuery
QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvOfflineGetInvoiceWordSetting','InvOfflineGetInvoiceWordSetting_RAT_0003', 'Query.csv')

query_info = EXEC_ACT(ACT_API.genOrderRequestInfoInvOfflineGetInvoiceWordSetting, QUERY_INFO_CSV)



query_rtn = EXEC_ACT(ACT_API.genPostRequestToAPIWordSetting, query_info)

query_rtn_dict = EXEC_ACT(ACT_API.strToDict, query_rtn)

data = EXEC_ACT(ACT_API.decryptDatab2c2, query_rtn_dict['Data'])

print(data)

#print InvoiceNo

# verification
#VERIFY(VER_API.verifyResponseValueb2c, CASE_NAME, data)
time.sleep(3)

INV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvOfflineIssue', CASE_NAME, 'Inv1.csv')


inv_info = EXEC_ACT(ACT_API1.genOrderRequestInfoB2c, INV_INFO_CSV,data)

api_response = EXEC_ACT(ACT_API1.genPostRequestToAPIOfflineIssue, inv_info)

res_dict = EXEC_ACT(ACT_API1.strToDict, api_response)

data1 = EXEC_ACT(ACT_API1.decryptDatab2c, res_dict['Data'])
print(data1)


# VERIFY
#VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME, 'success')

VERIFY(VER_API1.verifyResponseValuesb2c, CASE_NAME, data1)
time.sleep(3)






# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
