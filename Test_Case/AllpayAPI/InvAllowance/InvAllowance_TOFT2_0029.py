# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import os

#Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActInvIssue import actInvIssue
from Allpay.ProdActions.ActAllpayAPI.ActInvAllowance import actInvAllowance
from Allpay.Verification.VerifyAllpayAPI.VerifyInvAllowance import verifyInvAllowance


# (DO NO Edit) Static declare

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
ISSUE_API = actInvIssue()
ACT_API = actInvAllowance()
VER_API = verifyInvAllowance()

# Testing exec
# precondition-InvIssue
INV_ISSUE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvAllowance', 'Initial_Data', 'InvIssueWithoutPrint.csv')

exclusive_list = ['InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

revert_list = ['CustomerName', 'CustomerAddr', 'CustomerEmail', 'InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

inv_info = EXEC_ACT(ISSUE_API.genOrderRequestInfo, INV_ISSUE_INFO_CSV, exclusive_list, revert_list)

invoice_rtn = EXEC_ACT(ISSUE_API.genPostRequestToAPI, inv_info)

# InvAllowance
INV_ALLOWANCE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvAllowance', CASE_NAME, 'InvAllowance.csv')

invoice_rtn_dict = EXEC_ACT(ACT_API.strToDict, invoice_rtn)

exclusive_list = ['ItemName', 'ItemWord']

revert_list = ['CustomerName', 'NotifyMail', 'ItemName', 'ItemWord']

all_info = EXEC_ACT(ACT_API.genOrderRequestInfo, INV_ALLOWANCE_INFO_CSV, invoice_rtn_dict, exclusive_list, revert_list)

api_response = EXEC_ACT(ACT_API.genPostRequestToAPI, all_info)

res_dict = EXEC_ACT(ACT_API.strToDict, api_response)

# VERIFY
VERIFY(VER_API.verifyResponseValue, inv_info, invoice_rtn_dict, all_info, res_dict, CASE_NAME, 'success')


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
