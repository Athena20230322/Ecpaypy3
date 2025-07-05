# -*- coding: utf-8 -*-


# Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

# Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActInvIssue import actInvIssue
from Allpay.Verification.VerifyAllpayAPI.VerifyInvIssue import verifyInvIssue
from Allpay.ProdActions.ActAllpayAPI.ActInvAllowance import actInvAllowance
from Allpay.Verification.VerifyAllpayAPI.VerifyInvAllowance import verifyInvAllowance
from Allpay.ProdActions.ActAllpayAPI.ActInvQueryAllowance import actInvQueryAllowance
from Allpay.Verification.VerifyAllpayAPI.VerifyInvQueryAllowance import verifyInvQueryAllowance


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
ACT_ISSUE_API = actInvIssue()
VER_ISSUE_API = verifyInvIssue()
ACT_ALLOWANCE_API = actInvAllowance()
VER_ALLOWANCE_API = verifyInvAllowance()
ACT_API = actInvQueryAllowance()
VER_API = verifyInvQueryAllowance()

# Testing exec

# precondition-InvIssue

INV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvQueryAllowance', 'Initial_Data', 'Inv.csv')

exclusive_list = ['InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

revert_list = ['CustomerName', 'CustomerAddr', 'CustomerEmail', 'InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

inv_info = EXEC_ACT(ACT_ISSUE_API.genOrderRequestInfo, INV_INFO_CSV, exclusive_list, revert_list)

invoice_info = EXEC_ACT(ACT_ISSUE_API.genPostRequestToAPI, inv_info)

res_dict = EXEC_ACT(ACT_ISSUE_API.strToDict, invoice_info)

# precondition-InvIssue Verify

VERIFY(VER_ISSUE_API.verifyColumn, res_dict, 'InvIssue_RAT_0001')

# precondition-InvAllowance

INV_ALLOWANCE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvQueryAllowance', 'Initial_Data', 'InvAllowance.csv')

invoice_info_dict = EXEC_ACT(ACT_ALLOWANCE_API.strToDict, invoice_info)

exclusive_list = ['ItemName', 'ItemWord']

revert_list = ['CustomerName', 'NotifyMail', 'ItemName', 'ItemWord']

inv_info = EXEC_ACT(ACT_ALLOWANCE_API.genOrderRequestInfo, INV_ALLOWANCE_INFO_CSV, invoice_info_dict, exclusive_list, revert_list)

api_response = EXEC_ACT(ACT_ALLOWANCE_API.genPostRequestToAPI, inv_info)

res_dict = EXEC_ACT(ACT_ALLOWANCE_API.strToDict, api_response)

# precondition-InvAllowance VERIFY

VERIFY(VER_ALLOWANCE_API.verifyColumn, res_dict, 'InvAllowance_RAT_0001')

# print res_dict

Query_ALLOWANCE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvQueryAllowance', CASE_NAME, 'OrderInfo.csv')

inv_query_info = EXEC_ACT(ACT_API.genOrderRequestInfo, Query_ALLOWANCE_INFO_CSV, res_dict)

# print 'genOrderRequestInfo: ', inv_query_info

order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, inv_query_info)

VERIFY(VER_API.verifyInvQueryAllowanceResult, order_info_res, CASE_NAME)

# DRIVER.delete_all_cookies()
# DRIVER.quit()

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)