# -*- coding: utf-8 -*-


# Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActTradeNoAio import actTradeNoAio
from ECpay.Verification.VerifyECpayAPI.VerifyTradeNoAio import verifyTradeNoAio


# (DO NO Edit) Static declare

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
ACT_API = actTradeNoAio()
VER_API = verifyTradeNoAio()

# Testing exec

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'TradeNoAio', CASE_NAME, 'OrderInfo.csv')

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

order_info_tna_res = EXEC_ACT(ACT_API.genpostRequestToAPI, order_info)

order_info_tna_res_rtn_dict = EXEC_ACT(ACT_API.strToDict, order_info_tna_res)

time.sleep(5)

VERIFY(VER_API.verifyCSVReturn, order_info_tna_res_rtn_dict, CASE_NAME)

time.sleep(80)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)