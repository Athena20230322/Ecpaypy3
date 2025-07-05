# -*- coding: utf-8 -*-


# Static Import Area
import argparse
import os
import time

from  ECpay.ProdActions.ActECpayAPI.ActReturnCVS import actReturnCVS
from ECpay.Verification.VerifyECpayAPI.VerifyReturnCVS import verifyReturnCVS
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper

# (DO NO Edit) Static declare

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
DRIVER = clsWebDriverHelper().initWebDriver(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actReturnCVS()
VER_API = verifyReturnCVS()

# Testing exec

# Precondition create ECpay new order info

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnCVS', 'Initial_Data', 'AioCheckOut.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info, 'ChkoutEC_API')

# EXEC_ACT(ACT_API.inputPaymentPageCreditInfoEC, '4311-9522-2222-2222', '22', '05', '222', '0900000000')

# otp_info = EXEC_ACT(ACT_API.queryCreditOTP, '0900000000')

# EXEC_ACT(ACT_API.inputOTP, otp_info)

# Precondition create logistics order info

ORDER_INFO_CVS_CRT = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnCVS', 'Initial_Data', 'Create.csv')

order_info_crt = EXEC_ACT(ACT_API.genOrderRequestCreateCVS, ORDER_INFO_CVS_CRT, order_info['MerchantTradeNo'],
                          order_info['MerchantTradeDate'])

order_info_crt_res = EXEC_ACT(ACT_API.genpostRequestToAPI, order_info_crt,
                              'https://logistics-stage.ecpay.com.tw/Express/Create')

# Do ReturnCVS_API

ORDER_INFO_C2C = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnCVS', CASE_NAME, 'OrderInfo.csv')

EXEC_ACT(VER_API.enableWebOperate, DRIVER)

modify_str = EXEC_ACT(ACT_API.modifyAllpaylogisticsSplit, order_info_crt_res)

order_info_returncvs = EXEC_ACT(ACT_API.genOrderRequestCVS, ORDER_INFO_C2C, modify_str, True)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info_returncvs, 'ReturnCVS_API')

VERIFY(VER_API.verifyReturnCVSResult)

DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)