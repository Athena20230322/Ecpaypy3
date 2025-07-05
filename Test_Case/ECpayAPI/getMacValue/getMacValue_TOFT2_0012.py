# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper

import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActgetMacValue import actgetMacValue
from ECpay.Verification.VerifyECpayAPI.VerifygetMacValue import verifygetMacValue


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

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'getMacValue', CASE_NAME, 'OrderInfo.csv')

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

print(('order_info', order_info))

result1 = EXEC_ACT(ACT_API.createCheckMacValueByRequest, order_info)

print(('result1', result1))

result2 = EXEC_ACT(ACT_API.genCheckMacValue, order_info)

print(('result2', result2))

#VERIFY
VERIFY(VER_API.verifyDataWithApiAndGen, result1, result2)



# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)