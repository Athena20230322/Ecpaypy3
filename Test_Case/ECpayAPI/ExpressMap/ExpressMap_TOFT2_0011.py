# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActMockExpressMap import actMockExpressMap
from ECpay.Verification.VerifyECpayAPI.VerifyExpressMap import verifyExpressMap


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
DRIVER = clsWebDriverHelper().initWebDriver(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actMockExpressMap()
VER_API = verifyExpressMap()

#Testing exec
#precondition add new order
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'AioCheckOut', 'AioCheckOut_RAT_0002', 'OrderInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info)

#EXEC_ACT(ACT_API.inputPaymentPageCreditInfo, 'F128029956', '4311-9522-2222-2222', '22', '05', '222', '0900000000')

#otp_info= EXEC_ACT(ACT_API.queryCreditOTP, '0900000000')

#EXEC_ACT(ACT_API.inputOTP, otp_info)

MERC_T_NO = order_info['MerchantTradeNo']
time.sleep(3)

#ExpressMap
MAP_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ExpressMap', CASE_NAME, 'OrderInfo.csv')

map_req_info = EXEC_ACT(ACT_API.genOrderRequestInfo, MAP_INFO_CSV, MERC_T_NO)

EXEC_ACT(ACT_API.ExpressMapByBrowser, DRIVER, map_req_info)

time.sleep(2)

EXEC_ACT(ACT_API.ChooseHiLifeMockStore)

time.sleep(5)

DRIVER.delete_all_cookies()
DRIVER.quit()

response = EXEC_ACT(ACT_API.GetInfoFromServerReplyUrl, MERC_T_NO)

#VERIFY
VERIFY(VER_API.verifyHiLifeReturnResult, response, map_req_info)



# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)