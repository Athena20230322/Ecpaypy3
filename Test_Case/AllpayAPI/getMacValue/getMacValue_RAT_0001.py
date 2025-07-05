# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper

import os

#Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActgetMacValue import actgetMacValue
from Allpay.Verification.VerifyAllpayAPI.VerifygetMacValue import verifygetMacValue


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
ACT_API = actgetMacValue()
VER_API = verifygetMacValue()

#Testing exec

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'getMacValue', CASE_NAME, 'OrderInfo.csv')

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

print(('order_info', order_info))

result_from_api = EXEC_ACT(ACT_API.createCheckMacValueByRequest, order_info)

print(('result', result_from_api))

#VERIFY
VERIFY(VER_API.verifyApiServing, result_from_api)


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
