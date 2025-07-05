# -*- coding: utf-8 -*-

#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os
import sys
import importlib
importlib.reload(sys)

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActQueryTrade import actQueryTrade
from ECpay.Verification.VerifyECpayAPI.VerifyQueryTrade import verifyQueryTrade


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
ACT_API = actQueryTrade()
VER_API = verifyQueryTrade()

#Testing exec

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'QueryTrade', CASE_NAME, 'OrderInfo.csv')

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

#res = EXEC_ACT(ACT_API.createOrderByRequestThreeD, order_info)

order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, order_info)

res_dict = EXEC_ACT(ACT_API.strToDict, order_info_res)

data = EXEC_ACT(ACT_API.decryptData, res_dict['Data'])
print(data)

VERIFY(VER_API.verifyResponseValuesQueryThreeDQ, CASE_NAME, res_dict, data)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)