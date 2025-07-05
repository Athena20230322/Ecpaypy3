# -*- coding: utf-8 -*-


# Static Import Area
import argparse
import os
import time

from  ECpay.ProdActions.ActECpayAPI.ActReturnHome import actReturnHome
from ECpay.Verification.VerifyECpayAPI.VerifyReturnHome import verifyReturnHome
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper

#(DO NO Edit) Static declare

ARGP = argparse.ArgumentParser(description='Script for exec test.')
ARGP.add_argument('--logdir' , type=str, help = 'Specify the log dir')
ARGP.add_argument('--package' , type=str, help = 'Specify the package name')
ARGP.add_argument('--runid' , type=str , default='', help = 'Specify the runtime guid for this run.')
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

ACT_API = actReturnHome()
VER_API = verifyReturnHome()

# Testing exec

# Precondition create Allpay new order info

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnHome', 'Initial_Data', 'AioCheckOut.csv')

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.genpostRequestToAPI, order_info, 'ChkoutEC_API')

# Precondition create logistics order info

ORDER_INFO_CSV_CRT = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnHome', 'Initial_Data', 'Create_RAT_0001.csv')

order_info_crt = EXEC_ACT(ACT_API.genOrderRequestCreateHome, ORDER_INFO_CSV_CRT, order_info['MerchantTradeNo'],
                          order_info['MerchantTradeDate'])

order_info_crt_res = EXEC_ACT(ACT_API.genpostRequestToAPI, order_info_crt, 'Create_API')

# Do ReturnHome_API

ORDER_INFO_CSV_C2C = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnHome', CASE_NAME, 'OrderInfo.csv')

modify_str = EXEC_ACT(ACT_API.modifyAllpaylogisticsSplit, order_info_crt_res)

order_info_home = EXEC_ACT(ACT_API.genOrderRequestHome, ORDER_INFO_CSV_C2C, modify_str, "' or 1=1--")

order_info_rehome_res = EXEC_ACT(ACT_API.genpostRequestToAPI, order_info_home, 'ReHome_API')

VERIFY(VER_API.verifyStatusResult, order_info_rehome_res, '0|很抱歉，此帳號目前暫停使用，如有問題請洽客服協助。')

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)