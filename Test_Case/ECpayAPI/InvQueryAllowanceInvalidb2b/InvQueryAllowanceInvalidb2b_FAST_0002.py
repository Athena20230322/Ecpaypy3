# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvQueryAllowanceInvalidb2b import actInvQueryAllowanceInvalidb2b
from ECpay.Verification.VerifyECpayAPI.VerifyInvQueryAllowanceInvalidb2b import verifyInvQueryAllowanceInvalidb2b
from ECpay.ProdActions.ActECpayAPI.ActInvIssueb2b import actInvIssueb2b
from ECpay.Verification.VerifyECpayAPI.VerifyInvIssueb2b import verifyInvIssueb2b
from ECpay.ProdActions.ActECpayAPI.ActInvAllowanceb2b import actInvAllowanceb2b
from ECpay.Verification.VerifyECpayAPI.VerifyInvAllowanceb2b import verifyInvAllowanceb2b
from ECpay.ProdActions.ActECpayAPI.ActInvAllowanceInvalidb2b import actInvAllowanceInvalidb2b
from ECpay.Verification.VerifyECpayAPI.VerifyInvAllowanceInvalidb2b import verifyInvAllowanceInvalidb2b


#(DO NO Edit) Static declare

ARGP = argparse.ArgumentParser(description='Script for exec test.')
ARGP.add_argument('--logdir' , type=str, help = 'Specify the log dir')
ARGP.add_argument('--package' , type=str, help = 'Specify the package name')
ARGP.add_argument('--runid' , type=str , default='', help = 'Specify the runtime guid for this run.')
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
ACT_API = actInvQueryAllowanceInvalidb2b()
VER_API = verifyInvQueryAllowanceInvalidb2b()
ISS_API = actInvIssueb2b()
VER_ISS_API = verifyInvIssueb2b()
ALL_API = actInvAllowanceb2b()
VER_ALL_API = verifyInvAllowanceb2b()
ALL_INV_API = actInvAllowanceInvalidb2b()
VER_ALL_INV_API = verifyInvAllowanceInvalidb2b()

# Testing exec
# precondition-InvIssue
INV_ISSUE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryAllowanceInvalidb2b', 'Initial_Data', 'Inv.csv')

# exclusive_list = ['InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']
#
# revert_list = ['CustomerName', 'CustomerAddr', 'CustomerEmail', 'InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

inv_info = EXEC_ACT(ISS_API.genOrderRequestInfoB2B, INV_ISSUE_INFO_CSV)


inv_rtn = EXEC_ACT(ISS_API.genPostRequestToAPI, inv_info)


res_dict = EXEC_ACT(ISS_API.strToDict, inv_rtn)

data = EXEC_ACT(ISS_API.decryptDatab2b, res_dict['Data'])
print(data)

# precondition-InvIssue Verify

VERIFY(VER_ISS_API.verifyColumn,'InvIssueb2b_RAT_0001', data)

# precondition-InvAllowance
INV_ALLOWANCE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryAllowanceInvalidb2b', 'Initial_Data', 'InvAllowance.csv')

#inv_rtn_dict = EXEC_ACT(ALL_API.strToDict, inv_rtn)

# exclusive_list = ['ItemName', 'ItemWord']
#
# revert_list = ['CustomerName', 'NotifyMail', 'ItemName', 'ItemWord']

all_info = EXEC_ACT(ALL_API.genOrderRequestInfoB2B, INV_ALLOWANCE_INFO_CSV, data)

all_rtn = EXEC_ACT(ALL_API.genPostRequestToAPIb2b, all_info)

res_dict = EXEC_ACT(ALL_API.strToDict, all_rtn)

data = EXEC_ACT(ALL_API.decryptDatab2b, res_dict['Data'])
print(data)

# print 'all_rtn_dict Result:', all_rtn_dict

# precondition-InvAllowance VERIFY

VERIFY(VER_ALL_API.verifyColumn, 'InvAllowanceb2b_RAT_0001',data)

# precondition-InvAllowanceInvalid

INV_ALLOWNACE_INVALID_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryAllowanceInvalidb2b', 'Initial_Data', 'Invalid.csv')

# exclusive_list = ['Reason']
#
# revert_list = ['Reason']

invalid_info = EXEC_ACT(ALL_INV_API.genOrderRequestInfoB2B, INV_ALLOWNACE_INVALID_CSV,data)

invalid_rtn = EXEC_ACT(ALL_INV_API.genPostRequestToAPI, invalid_info)

data1 = EXEC_ACT(ALL_API.decryptDatab2b, invalid_info['Data'])

#invalid_rtn_dict = EXEC_ACT(ALL_API.strToDict, invalid_rtn)

res_dict = EXEC_ACT(ALL_API.strToDict, invalid_rtn)

data = EXEC_ACT(ALL_API.decryptDatab2b, res_dict['Data'])

# print 'invalid_rtn_dict Result:', inv_rtn_dict

# precondition-InvAllowanceInvalid verification

VERIFY(VER_ALL_INV_API.verifyColumn, 'InvAllowanceInvalidb2b_RAT_0001',data)

# InvQueryAllowanceInvalid

Query_ALLINVALID_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryAllowanceInvalidb2b', CASE_NAME, 'OrderInfo.csv')

inv_query_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2B, Query_ALLINVALID_INFO_CSV, data,data1)

# print 'genOrderRequestInfo: ', inv_query_info

order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, inv_query_info)

res_dict = EXEC_ACT(ALL_API.strToDict, order_info_res)

data = EXEC_ACT(ALL_API.decryptDatab2b2, res_dict['Data'])

VERIFY(VER_API.verifyQueryAllowInvalidRequestInfob2b,data)

# DRIVER.delete_all_cookies()
# DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)