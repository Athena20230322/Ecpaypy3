# -*- coding: utf-8 -*-


# Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

# Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvIssue import actInvIssue
from ECpay.ProdActions.ActECpayAPI.ActInvIssueInvalid import actInvIssueInvalid
from ECpay.Verification.VerifyECpayAPI.VerifyInvIssue import verifyInvIssue
from ECpay.Verification.VerifyECpayAPI.VerifyInvIssueInvalid import verifyInvIssueInvalid


# (DO NO Edit) Static declare

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
ACT_API = actInvIssueInvalid()
VER_API = verifyInvIssueInvalid()
ACT_ISSUE_API = actInvIssue()
VER_ISSUE_API = verifyInvIssue()

# Testing exec

# InvIssue

INV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvIssue', 'InvIssue_RAT_0001', 'Inv.csv')

exclusive_list = ['InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

revert_list = ['CustomerName', 'CustomerAddr', 'CustomerEmail', 'InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

inv_info = EXEC_ACT(ACT_ISSUE_API.genOrderRequestInfo, INV_INFO_CSV, exclusive_list, revert_list)

api_response = EXEC_ACT(ACT_ISSUE_API.genPostRequestToAPI, inv_info)

res_dict = EXEC_ACT(ACT_ISSUE_API.strToDict, api_response)

# Verify

VERIFY(VER_ISSUE_API.verifyColumn, res_dict, 'InvIssue_RAT_0001')

# InvIssueInvalid

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvIssueInvalid', CASE_NAME, 'OrderInfo.csv')

revert_list = ['Reason']

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV, res_dict['InvoiceNumber'], revert_list)

order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, order_info)

res_issue_invalid_dict = EXEC_ACT(ACT_API.strToDict, order_info_res)

VERIFY(VER_API.verifyColumn, res_issue_invalid_dict, CASE_NAME)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)