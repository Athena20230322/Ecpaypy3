# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActInvAllowance import actInvAllowance
from Allpay.ProdActions.ActAllpayAPI.ActInvIssue import actInvIssue
from Allpay.ProdActions.ActAllpayAPI.ActInvQuery import actInvQuery
from Allpay.Verification.VerifyAllpayAPI.VerifyInvQuery import verifyInvQuery


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
ISSUE_API = actInvIssue()
ALL_API = actInvAllowance()
ACT_API = actInvQuery()
VER_API = verifyInvQuery()

# Testing exec
# precondition-InvIssue
INV_ISSUE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvQuery', 'Initial_Data', 'InvIssue.csv')

exclusive_list = ['InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

revert_list = ['CustomerName', 'CustomerAddr', 'CustomerEmail', 'InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

inv_info = EXEC_ACT(ISSUE_API.genOrderRequestInfo, INV_ISSUE_INFO_CSV, exclusive_list, revert_list)

invoice_rtn = EXEC_ACT(ISSUE_API.genPostRequestToAPI, inv_info)

inv_rtn_dict = EXEC_ACT(ISSUE_API.strToDict, invoice_rtn)

# precondition-InvAllowance
INV_ALLOWANCE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvAllowance', 'InvAllowance_RAT_0001', 'InvAllowance.csv')

all_exclusive_list = ['ItemName', 'ItemWord']

all_revert_list = ['CustomerName', 'NotifyMail', 'ItemName', 'ItemWord']

inv_all_info = EXEC_ACT(ALL_API.genOrderRequestInfo, INV_ALLOWANCE_INFO_CSV, inv_rtn_dict, all_exclusive_list, all_revert_list)

api_response = EXEC_ACT(ALL_API.genPostRequestToAPI, inv_all_info)

all_dict = EXEC_ACT(ALL_API.strToDict, api_response)

# InvQuery
QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvQuery', CASE_NAME, 'Query.csv')

query_info = EXEC_ACT(ACT_API.genOrderRequestInfo, QUERY_INFO_CSV, inv_info)

query_rtn = EXEC_ACT(ACT_API.genPostRequestToAPI, query_info)

query_rtn_dict = EXEC_ACT(ISSUE_API.strToDict, query_rtn)

certain_keys = []

inv_info = EXEC_ACT(ISSUE_API.quote_item, inv_info, revert_list)

# verification
VERIFY(VER_API.verifyCertainResponseValue, query_rtn_dict, inv_info, inv_rtn_dict, CASE_NAME, certain_keys)

VERIFY(VER_API.verifyAllowance, query_rtn_dict, all_dict)


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
