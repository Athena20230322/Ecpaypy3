# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvDelayb2c import actInvDelayb2c
from ECpay.Verification.VerifyECpayAPI.VerifyInvDelayb2c import verifyInvDelayb2c


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
# DRIVER = clsWebDriverHelper().initWebDriver(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actInvDelayb2c()
VER_API = verifyInvDelayb2c()

#Testing exec

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvDelayb2c', CASE_NAME, 'OrderInfo.csv')

order_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2citem, ORDER_INFO_CSV)

order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, order_info)

res_dict = EXEC_ACT(ACT_API.strToDict, order_info_res)

data = EXEC_ACT(ACT_API.decryptDatab2c2, res_dict['Data'])
print(data)

VERIFY(VER_API.verifyInvDelayRequestInfo,data,CASE_NAME)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)