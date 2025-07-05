# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvIssueByPlatform import actInvIssueByPlatform
from ECpay.Verification.VerifyECpayAPI.VerifyInvIssueByPlatform import verifyInvIssueByPlatform


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
ACT_API = actInvIssueByPlatform()
VER_API = verifyInvIssueByPlatform()

#Testing exec

INV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvIssueByPlatform', CASE_NAME, 'Inv.csv')

exclusive_list = ['InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

revert_list = ['CustomerName', 'CustomerAddr', 'CustomerEmail', 'InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

inv_info = EXEC_ACT(ACT_API.genOrderRequestInfo, INV_INFO_CSV, exclusive_list, revert_list)

api_response = EXEC_ACT(ACT_API.genPostRequestToAPI, inv_info)

res_dict = EXEC_ACT(ACT_API.strToDict, api_response)

# VERIFY
VERIFY(VER_API.verifyResponseValueError, res_dict, CASE_NAME, 'success')


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
