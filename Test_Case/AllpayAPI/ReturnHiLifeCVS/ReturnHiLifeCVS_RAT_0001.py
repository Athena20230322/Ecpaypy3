# -*- coding: utf-8 -*-


# Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

# Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActReturnHiLifeCVS import actReturnHiLifeCVS
from Allpay.Verification.VerifyAllpayAPI.VerifyReturnHiLifeCVS import verifyReturnHiLifeCVS

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
ACT_API = actReturnHiLifeCVS()
VER_API = verifyReturnHiLifeCVS()

# Testing exec

# Precondition create Allpay new order info

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'ReturnHiLifeCVS', 'Initial_Data', 'AioCheckOut.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)
EXEC_ACT(VER_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info, 'ChkoutAP_API')

# EXEC_ACT(ACT_API.inputPaymentPageCreditInfoAP, 'A129618149', '4311-9522-2222-2222', '22', '05', '222', '0963957452')

# otp_info = EXEC_ACT(ACT_API.queryCreditOTP, '0922652130')

# EXEC_ACT(ACT_API.inputOTP, otp_info)

# Precondition create logistics order info

ORDER_INFO_CVS_CRT = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'ReturnHiLifeCVS', 'Initial_Data', 'Create.csv')

order_info_crt = EXEC_ACT(ACT_API.genOrderRequestCreateCVS, ORDER_INFO_CVS_CRT, order_info['MerchantTradeNo'],
                          order_info['MerchantTradeDate'])

order_info_crt_res = EXEC_ACT(ACT_API.genpostRequestToAPI, order_info_crt, 'Create_API')

# Do ReturnCVS_API

ORDER_INFO_C2C = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'ReturnHiLifeCVS', CASE_NAME, 'OrderInfo.csv')

modify_str = EXEC_ACT(ACT_API.modifyAllpaylogisticsSplit, order_info_crt_res)

order_info_returncvs = EXEC_ACT(ACT_API.genOrderRequestCVS, ORDER_INFO_C2C, modify_str, False, True)

response = EXEC_ACT(ACT_API.genpostRequestToAPI, order_info_returncvs, 'ReturnHiLifeCVS_API')

VERIFY(VER_API.verifyReturnCVSStrResult, response)

DRIVER.delete_all_cookies()
DRIVER.quit()

# # Precondition create new HiLifeTestData
#
# ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnHiLifeCVS', 'Initial_Data', 'HiLifeTestData.csv')
#
# order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)
#
# order_info_crt_res = EXEC_ACT(ACT_API.genpostRequestToAPI, order_info, 'CreateHiLife_API')
#
# # Do ReturnHiLifeCVS_API
#
# ORDER_INFO_B2C = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnHiLifeCVS', CASE_NAME, 'OrderInfo.csv')
#
# # EXEC_ACT(VER_API.enableWebOperate, DRIVER)
#
# modify_str = EXEC_ACT(ACT_API.modifyAllpaylogisticsSplit, order_info_crt_res)
#
# order_info_returnhilifecvs = EXEC_ACT(ACT_API.genOrderRequestCVS, ORDER_INFO_B2C, modify_str)
#
# response = EXEC_ACT(ACT_API.genpostRequestToAPI, order_info_returnhilifecvs, 'ReturnHiLifeCVS_API')
#
# # EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info_returnhilifecvs, 'ReturnHiLifeCVS_API')
#
# VERIFY(VER_API.verifyReturnCVSStrResult, response)
#
# # DRIVER.delete_all_cookies()
# # DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)