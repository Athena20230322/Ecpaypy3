# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActInvIssue import actInvIssue
from Allpay.ProdActions.ActAllpayAPI.ActInvAllowance import actInvAllowance
from Allpay.ProdActions.ActAllpayAPI.ActInvAllowanceInvalid import actInvAllowanceInvalid
from Allpay.Verification.VerifyAllpayAPI.VerifyInvAllowanceInvalid import verifyInvAllowanceInvalid


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
ISS_API = actInvIssue()
ALL_API = actInvAllowance()
ACT_API = actInvAllowanceInvalid()
VER_API = verifyInvAllowanceInvalid()

# Testing exec
# precondition-InvIssue
INV_ISSUE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvAllowanceInvalid', 'Initial_Data', 'InvIssue.csv')

exclusive_list = ['InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

revert_list = ['CustomerName', 'CustomerAddr', 'CustomerEmail', 'InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

inv_info = EXEC_ACT(ISS_API.genOrderRequestInfo, INV_ISSUE_INFO_CSV, exclusive_list, revert_list)

inv_rtn = EXEC_ACT(ISS_API.genPostRequestToAPI, inv_info)

# precondition-InvAllowance
INV_ALLOWANCE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvAllowanceInvalid', 'Initial_Data', 'InvAllowance.csv')

inv_rtn_dict = EXEC_ACT(ALL_API.strToDict, inv_rtn)

exclusive_list = ['ItemName', 'ItemWord']

revert_list = ['CustomerName', 'NotifyMail', 'ItemName', 'ItemWord']

all_info = EXEC_ACT(ALL_API.genOrderRequestInfo, INV_ALLOWANCE_INFO_CSV, inv_rtn_dict, exclusive_list, revert_list)

all_rtn = EXEC_ACT(ALL_API.genPostRequestToAPI, all_info)

all_rtn_dict = EXEC_ACT(ALL_API.strToDict, all_rtn)

# InvAllowanceInvalid
INV_ALLOWNACE_INVALID_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvAllowanceInvalid', CASE_NAME, 'Invalid.csv')

exclusive_list = ['Reason']

revert_list = ['Reason']

invalid_info = EXEC_ACT(ACT_API.genOrderRequestInfo, INV_ALLOWNACE_INVALID_CSV, all_rtn_dict, exclusive_list, revert_list)

invalid_rtn = EXEC_ACT(ACT_API.genPostRequestToAPI, invalid_info)

invalid_rtn_dict = EXEC_ACT(ALL_API.strToDict, invalid_rtn)

gen_result = EXEC_ACT(ACT_API.genCheckMacValue, invalid_rtn_dict)

# verification
VERIFY(VER_API.verifyCheckMacValue, invalid_rtn_dict, gen_result)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
