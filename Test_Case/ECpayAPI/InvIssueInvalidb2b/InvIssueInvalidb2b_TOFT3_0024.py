# -*- coding: utf-8 -*-


# Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

# Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvIssueb2b import actInvIssueb2b
from ECpay.ProdActions.ActECpayAPI.ActInvIssueInvalidb2b import actInvIssueInvalidb2b
from ECpay.Verification.VerifyECpayAPI.VerifyInvIssueb2b import verifyInvIssueb2b
from ECpay.Verification.VerifyECpayAPI.VerifyInvIssueInvalidb2b import verifyInvIssueInvalidb2b


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

ACT_API = actInvIssueInvalidb2b()
VER_API = verifyInvIssueInvalidb2b()
ACT_ISSUE_API = actInvIssueb2b()
VER_ISSUE_API = verifyInvIssueb2b()

# Testing exec

# InvIssue

INV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvIssueb2b', 'InvIssueb2b_RAT_0001', 'Inv.csv')

#exclusive_list = ['InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

#revert_list = ['CustomerName', 'CustomerAddr', 'CustomerEmail', 'InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

inv_info = EXEC_ACT(ACT_ISSUE_API.genOrderRequestInfoB2B, INV_INFO_CSV)

data1 = EXEC_ACT(ACT_ISSUE_API.decryptDatab2b, inv_info['Data'])

api_response = EXEC_ACT(ACT_ISSUE_API.genPostRequestToAPI, inv_info)

res_dict = EXEC_ACT(ACT_ISSUE_API.strToDict, api_response)

data = EXEC_ACT(ACT_ISSUE_API.decryptDatab2b, res_dict['Data'])
print(data)


# Verify

VERIFY(VER_ISSUE_API.verifyColumn, 'InvIssueb2b_RAT_0001', data)

# InvIssueInvalid

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvIssueInvalidb2b', CASE_NAME, 'OrderInfo.csv')

revert_list = ['Reason']

order_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2B, ORDER_INFO_CSV, data,data1,"' or 1=1--")

order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPIb2b, order_info)

# Verify

#VERIFY(VER_API.verifyInvIssueInvalidResult, order_info_res, CASE_NAME)

VERIFY(VER_API.verifyResponseValuesb2b, CASE_NAME, data)

time.sleep(3)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)