# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActInvDelay import actInvDelay
from Allpay.ProdActions.ActAllpayAPI.ActInvTrigger import actInvTrigger
from Allpay.Verification.VerifyAllpayAPI.VerifyInvTrigger import verifyInvTrigger


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
DELAY_API = actInvDelay()
ACT_API = actInvTrigger()
VER_API = verifyInvTrigger()

# Testing exec
# precondition-InvDelay
DELAY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvTrigger', 'Initial_Data', 'InvDelay1Day.csv')

exclusive_args = ['InvoiceRemark', 'ItemName', 'ItemWord']

revert_args = ['CustomerName', 'CustomerAddr', 'CustomerEmail', 'InvoiceRemark', 'ItemName', 'ItemWord']

delay_issue_info = EXEC_ACT(DELAY_API.genOrderRequestInfo, DELAY_INFO_CSV, revert_args, exclusive_args)

delay_rtn = EXEC_ACT(DELAY_API.genPostRequestToAPI, delay_issue_info)

# InvTrigger
delay_rtn_dict = EXEC_ACT(ACT_API.strToDict, delay_rtn)

TRIGGER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'InvTrigger', CASE_NAME, 'InvTrigger.csv')

trigger_info = EXEC_ACT(ACT_API.genOrderRequestInfo, TRIGGER_INFO_CSV, delay_rtn_dict)

trigger_rtn = EXEC_ACT(ACT_API.genPostRequestToAPI, trigger_info)

trigger_rtn_dict = EXEC_ACT(ACT_API.strToDict, trigger_rtn)

check_mac_value = EXEC_ACT(ACT_API.genCheckMacValue, trigger_rtn_dict)

# verification
VERIFY(VER_API.verifyResponseValue, trigger_rtn_dict, delay_rtn_dict, CASE_NAME)

VERIFY(VER_API.verifyChkValue, trigger_rtn_dict, check_mac_value)



# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
