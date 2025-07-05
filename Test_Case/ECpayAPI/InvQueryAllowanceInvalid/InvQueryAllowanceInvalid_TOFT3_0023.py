# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvQueryAllowanceInvalid import actInvQueryAllowanceInvalid
from ECpay.Verification.VerifyECpayAPI.VerifyInvQueryAllowanceInvalid import verifyInvQueryAllowanceInvalid
from ECpay.ProdActions.ActECpayAPI.ActInvIssue import actInvIssue
from ECpay.Verification.VerifyECpayAPI.VerifyInvIssue import verifyInvIssue
from ECpay.ProdActions.ActECpayAPI.ActInvAllowance import actInvAllowance
from ECpay.Verification.VerifyECpayAPI.VerifyInvAllowance import verifyInvAllowance
from ECpay.ProdActions.ActECpayAPI.ActInvAllowanceInvalid import actInvAllowanceInvalid
from ECpay.Verification.VerifyECpayAPI.VerifyInvAllowanceInvalid import verifyInvAllowanceInvalid


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
ACT_API = actInvQueryAllowanceInvalid()
VER_API = verifyInvQueryAllowanceInvalid()
ISS_API = actInvIssue()
VER_ISS_API = verifyInvIssue()
ALL_API = actInvAllowance()
VER_ALL_API = verifyInvAllowance()
ALL_INV_API = actInvAllowanceInvalid()
VER_ALL_INV_API = verifyInvAllowanceInvalid()

# Testing exec
# precondition-InvIssue
INV_ISSUE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryAllowanceInvalid', 'Initial_Data', 'Inv.csv')

exclusive_list = ['InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

revert_list = ['CustomerName', 'CustomerAddr', 'CustomerEmail', 'InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

inv_info = EXEC_ACT(ISS_API.genOrderRequestInfo, INV_ISSUE_INFO_CSV, exclusive_list, revert_list)

inv_rtn = EXEC_ACT(ISS_API.genPostRequestToAPI, inv_info)

res_dict = EXEC_ACT(ISS_API.strToDict, inv_rtn)

# precondition-InvIssue Verify

VERIFY(VER_ISS_API.verifyColumn, res_dict, 'InvIssue_RAT_0001')

# precondition-InvAllowance
INV_ALLOWANCE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryAllowanceInvalid', 'Initial_Data', 'InvAllowance.csv')

inv_rtn_dict = EXEC_ACT(ALL_API.strToDict, inv_rtn)

exclusive_list = ['ItemName', 'ItemWord']

revert_list = ['CustomerName', 'NotifyMail', 'ItemName', 'ItemWord']

all_info = EXEC_ACT(ALL_API.genOrderRequestInfo, INV_ALLOWANCE_INFO_CSV, inv_rtn_dict, exclusive_list, revert_list)

all_rtn = EXEC_ACT(ALL_API.genPostRequestToAPI, all_info)

all_rtn_dict = EXEC_ACT(ALL_API.strToDict, all_rtn)

# print 'all_rtn_dict Result:', all_rtn_dict

# precondition-InvAllowance VERIFY

VERIFY(VER_ALL_API.verifyColumn, all_rtn_dict, 'InvAllowance_RAT_0001')

# precondition-InvAllowanceInvalid

INV_ALLOWNACE_INVALID_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryAllowanceInvalid', 'Initial_Data', 'Invalid.csv')

exclusive_list = ['Reason']

revert_list = ['Reason']

invalid_info = EXEC_ACT(ALL_INV_API.genOrderRequestInfo, INV_ALLOWNACE_INVALID_CSV, all_rtn_dict, exclusive_list, revert_list)

invalid_rtn = EXEC_ACT(ALL_INV_API.genPostRequestToAPI, invalid_info)

invalid_rtn_dict = EXEC_ACT(ALL_API.strToDict, invalid_rtn)

# print 'invalid_rtn_dict Result:', inv_rtn_dict

# precondition-InvAllowanceInvalid verification

VERIFY(VER_ALL_INV_API.verifyColumn, invalid_rtn_dict, 'InvAllowanceInvalid_RAT_0001')

# InvQueryAllowanceInvalid

Query_ALLINVALID_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryAllowanceInvalid', CASE_NAME, 'OrderInfo.csv')

inv_query_info = EXEC_ACT(ACT_API.genOrderRequestInfo, Query_ALLINVALID_INFO_CSV, all_rtn_dict, "hi' or 1=1--")

# print 'genOrderRequestInfo: ', inv_query_info

order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, inv_query_info)

VERIFY(VER_API.verifyStatusResult, order_info_res, '查無折讓單資料，請確認!')

# DRIVER.delete_all_cookies()
# DRIVER.quit()

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)