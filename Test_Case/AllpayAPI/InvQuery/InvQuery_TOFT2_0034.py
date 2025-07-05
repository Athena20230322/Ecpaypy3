# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActInvIssue import actInvIssue
from Allpay.ProdActions.ActAllpayAPI.ActInvIssueInvalid import actInvIssueInvalid
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
INVALID_API = actInvIssueInvalid()
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

#precondition-InvIssueInvalid
INVALID_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvQuery', 'Initial_Data', 'InvIssueInvalid.csv')

invalid_revert = ['Reason']

invalid_info = EXEC_ACT(INVALID_API.genOrderRequestInfo, INVALID_INFO_CSV, inv_rtn_dict['InvoiceNumber'], invalid_revert)

invalid_rtn = EXEC_ACT(INVALID_API.genpostRequestToAPI, invalid_info,
                       'https://einvoice-stage.allpay.com.tw/Invoice/IssueInvalid')

# InvQuery
QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvQuery', CASE_NAME, 'Query.csv')

query_info = EXEC_ACT(ACT_API.genOrderRequestInfo, QUERY_INFO_CSV, inv_info)

query_rtn = EXEC_ACT(ACT_API.genPostRequestToAPI, query_info)

query_rtn_dict = EXEC_ACT(ISSUE_API.strToDict, query_rtn)

certain_keys = []

inv_info = EXEC_ACT(ISSUE_API.quote_item, inv_info, revert_list)

# verification
VERIFY(VER_API.verifyCertainResponseValue, query_rtn_dict, inv_info, inv_rtn_dict, CASE_NAME, certain_keys)

VERIFY(VER_API.verifyFlag, query_rtn_dict, 'IIS_Invalid_Status', '1')


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
