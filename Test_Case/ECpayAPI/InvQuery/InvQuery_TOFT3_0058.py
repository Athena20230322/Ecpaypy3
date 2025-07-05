# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvIssue import actInvIssue
from ECpay.ProdActions.ActECpayAPI.ActInvQuery import actInvQuery
from ECpay.Verification.VerifyECpayAPI.VerifyInvQuery import verifyInvQuery


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
ACT_API = actInvQuery()
VER_API = verifyInvQuery()

# Testing exec
# InvQuery
QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQuery', CASE_NAME, 'Query.csv')

query_info = EXEC_ACT(ACT_API.genOrderRequestInfo, QUERY_INFO_CSV, {})

query_rtn = EXEC_ACT(ACT_API.genPostRequestToAPI, query_info)

query_rtn_dict = EXEC_ACT(ISSUE_API.strToDict, query_rtn)

# verification
VERIFY(VER_API.verifyInjection, query_rtn_dict, query_info, CASE_NAME)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
