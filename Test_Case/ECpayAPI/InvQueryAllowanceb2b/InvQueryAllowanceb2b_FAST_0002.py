# -*- coding: utf-8 -*-


# Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

# Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvIssueb2b import actInvIssueb2b
from ECpay.Verification.VerifyECpayAPI.VerifyInvIssueb2b import verifyInvIssueb2b
from ECpay.ProdActions.ActECpayAPI.ActInvAllowanceb2b import actInvAllowanceb2b
from ECpay.Verification.VerifyECpayAPI.VerifyInvAllowanceb2b import verifyInvAllowanceb2b
from ECpay.ProdActions.ActECpayAPI.ActInvQueryAllowanceb2b import actInvQueryAllowanceb2b
from ECpay.Verification.VerifyECpayAPI.VerifyInvQueryAllowanceb2b import verifyInvQueryAllowanceb2b


#(DO NO Edit) Static declare

ARGP = argparse.ArgumentParser(description='Script for exec test.')
ARGP.add_argument('--logdir', type=str, help='Specify the log dir')
ARGP.add_argument('--package', type=str, help='Specify the package name')
ARGP.add_argument('--runid', type=str, default='', help = 'Specify the runtime guid for this run.')
ARGS = ARGP.parse_args()
LOG_DIR = ARGS.logdir
PKG = ARGS.package
RUN_UID = ARGS.runid
CASE_NAME = str(os.path.basename(__file__)).rstrip('.py')
SUM_LOG = os.path.join(LOG_DIR, CASE_NAME, 'Summary.log')
HELPER = classTestHelper(SUM_LOG)
# DRIVER = clsWebDriverHelper().initWebDriver(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_ISSUE_API = actInvIssueb2b()
VER_ISSUE_API = verifyInvIssueb2b()
ACT_ALLOWANCE_API = actInvAllowanceb2b()
VER_ALLOWANCE_API = verifyInvAllowanceb2b()
ACT_API = actInvQueryAllowanceb2b()
VER_API = verifyInvQueryAllowanceb2b()

# Testing exec

# precondition-InvIssue

INV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryAllowanceb2b', 'Initial_Data', 'Inv.csv')



inv_info = EXEC_ACT(ACT_ISSUE_API.genOrderRequestInfoB2B, INV_INFO_CSV)

invoice_rtn = EXEC_ACT(ACT_ISSUE_API.genPostRequestToAPI, inv_info)

res_dict = EXEC_ACT(ACT_ISSUE_API.strToDict, invoice_rtn)

data = EXEC_ACT(ACT_ISSUE_API.decryptDatab2b, res_dict['Data'])
print(data)

# precondition-InvIssue Verify

VERIFY(VER_ISSUE_API.verifyColumn, 'InvIssueb2b_RAT_0001', data)

# precondition-InvAllowance

INV_ALLOWANCE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryAllowanceb2b', 'Initial_Data', 'InvAllowance.csv')


inv_info = EXEC_ACT(ACT_ALLOWANCE_API.genOrderRequestInfoB2B, INV_ALLOWANCE_INFO_CSV, data)



api_response = EXEC_ACT(ACT_ALLOWANCE_API.genPostRequestToAPIb2b, inv_info)

res_dict = EXEC_ACT(ACT_ALLOWANCE_API.strToDict, api_response)

data = EXEC_ACT(ACT_ALLOWANCE_API.decryptDatab2b, res_dict['Data'])
print(data)


# precondition-InvAllowance VERIFY

VERIFY(VER_ALLOWANCE_API.verifyColumn, 'InvAllowanceb2b_RAT_0001', data)



# print res_dict

Query_ALLOWANCE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryAllowanceb2b', CASE_NAME, 'OrderInfo.csv')



inv_query_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2B, Query_ALLOWANCE_INFO_CSV, data)

# print 'genOrderRequestInfo: ', inv_query_info

order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPIb2b, inv_query_info)

res_dict = EXEC_ACT(ACT_ALLOWANCE_API.strToDict, order_info_res)

data = EXEC_ACT(ACT_ALLOWANCE_API.decryptDatab2b2, res_dict['Data'])

#VERIFY(VER_API.verifyInvQueryAllowanceResultb2c, CASE_NAME,data)

VERIFY(VER_API.verifyInvQueryAllowanceRequestInfo, data)

VERIFY(VER_API.verifyInvQueryAllowanceResultb2b,data,CASE_NAME)
# DRIVER.delete_all_cookies(
# DRIVER.quit()

#VERIFY(VER_API.verifyResponseValueb2c, CASE_NAME, data)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)