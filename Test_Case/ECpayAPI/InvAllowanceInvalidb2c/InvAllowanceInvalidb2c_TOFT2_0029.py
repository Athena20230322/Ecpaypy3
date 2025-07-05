# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvIssueb2c import actInvIssueb2c
from ECpay.ProdActions.ActECpayAPI.ActInvAllowanceb2c import actInvAllowanceb2c
from ECpay.ProdActions.ActECpayAPI.ActInvAllowanceInvalidb2c import actInvAllowanceInvalidb2c
from ECpay.Verification.VerifyECpayAPI.VerifyInvAllowanceInvalidb2c import verifyInvAllowanceInvalidb2c


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
ISS_API = actInvIssueb2c()
ALL_API = actInvAllowanceb2c()
ACT_API = actInvAllowanceInvalidb2c()
VER_API = verifyInvAllowanceInvalidb2c()

# Testing exec
# precondition-InvIssue
INV_ISSUE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvAllowanceInvalidb2c', 'Initial_Data', 'InvIssue.csv')

exclusive_list = ['InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

revert_list = ['CustomerName', 'CustomerAddr', 'CustomerEmail', 'InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

inv_info = EXEC_ACT(ISS_API.genOrderRequestInfoB2c, INV_ISSUE_INFO_CSV)

inv_rtn = EXEC_ACT(ISS_API.genPostRequestToAPI, inv_info)

#api_response = EXEC_ACT(ISS_API.genPostRequestToAPI, inv_info)

res_dict = EXEC_ACT(ISS_API.strToDict, inv_rtn)

data = EXEC_ACT(ISS_API.decryptDatab2c, res_dict['Data'])
print(data)

# precondition-InvAllowance
INV_ALLOWANCE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvAllowanceInvalidb2c', 'Initial_Data', 'InvAllowance.csv')

all_info = EXEC_ACT(ALL_API.genOrderRequestInfoB2c, INV_ALLOWANCE_INFO_CSV,data)

all_rtn = EXEC_ACT(ALL_API.genPostRequestToAPIb2c, all_info)

all_rtn_dict = EXEC_ACT(ALL_API.strToDict, all_rtn)


data = EXEC_ACT(ALL_API.decryptDatab2c, all_rtn_dict['Data'])
print(data)

# InvAllowanceInvalid
INV_ALLOWNACE_INVALID_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvAllowanceInvalidb2c', CASE_NAME, 'Invalid.csv')


invalid_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2c, INV_ALLOWNACE_INVALID_CSV,data)

invalid_rtn = EXEC_ACT(ACT_API.genPostRequestToAPI, invalid_info)

invalid_rtn_dict = EXEC_ACT(ALL_API.strToDict, invalid_rtn)

data = EXEC_ACT(ALL_API.decryptDatab2c, invalid_rtn_dict['Data'])
print(data)

# verification
#VERIFY(VER_API.verifyResponseValue, invalid_rtn_dict, all_rtn_dict, CASE_NAME)

# VERIFY(VER_API.verifyResponseValuesb2c, CASE_NAME, data)
#
# time.sleep(10)


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
