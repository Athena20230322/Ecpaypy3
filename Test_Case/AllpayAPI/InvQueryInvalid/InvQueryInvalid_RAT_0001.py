# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActInvIssue import actInvIssue
from Allpay.ProdActions.ActAllpayAPI.ActInvIssueInvalid import actInvIssueInvalid
from Allpay.ProdActions.ActAllpayAPI.ActInvQueryInvalid import actInvQueryInvalid
from Allpay.Verification.VerifyAllpayAPI.VerifyInvQueryInvalid import verifyInvQueryInvalid


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
ACT_API = actInvQueryInvalid()
VER_API = verifyInvQueryInvalid()

# Testing exec
# precondition-InvIssue
ISSUE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvQueryInvalid', 'Initial_Data', 'InvIssue.csv')

exclusive_list = ['InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

revert_list = ['CustomerName', 'CustomerAddr', 'CustomerEmail', 'InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

issue_info = EXEC_ACT(ISSUE_API.genOrderRequestInfo, ISSUE_INFO_CSV, exclusive_list, revert_list)

issue_rtn = EXEC_ACT(ISSUE_API.genPostRequestToAPI, issue_info)

issue_rtn_dict = EXEC_ACT(ISSUE_API.strToDict, issue_rtn)

# precondition-InvIssueInvalid
INVALID_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvQueryInvalid', 'Initial_Data', 'InvIssueInvalid.csv')

invalid_revert = ['Reason']

invalid_info = EXEC_ACT(INVALID_API.genOrderRequestInfo, INVALID_INFO_CSV, issue_rtn_dict['InvoiceNumber'], invalid_revert)

invalid_rtn = EXEC_ACT(INVALID_API.genpostRequestToAPI, invalid_info,
                       'https://einvoice-stage.allpay.com.tw/Invoice/IssueInvalid')

# InvQueryInvalid
QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvQueryInvalid', CASE_NAME, 'InvQueryInvalid.csv')

query_info = EXEC_ACT(ACT_API.genOrderRequestInfo, QUERY_INFO_CSV, issue_info)

query_rtn = EXEC_ACT(ACT_API.genPostRequestToAPI, query_info)

query_rtn_dict = EXEC_ACT(ISSUE_API.strToDict, query_rtn)

# verification
VERIFY(VER_API.verifyColumn, query_rtn_dict, CASE_NAME)


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
