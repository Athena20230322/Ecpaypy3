# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActExpressMap import actExpressMap
from Allpay.ProdActions.ActAllpayAPI.ActAioCheckOut import actAioCheckOut
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
ORDER_API = actAioCheckOut()
ACT_API = actExpressMap()
VER_API = verifyExpressMap()

#Testing exec
#precondition add new order
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'AioCheckOut', 'AioCheckOut_RAT_0002', 'OrderInfo.csv')

EXEC_ACT(ORDER_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ORDER_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ORDER_API.createOrderByBrowser, DRIVER, order_info)

#EXEC_ACT(ORDER_API.inputPaymentPageCreditInfo, 'F128029956', '4311-9522-2222-2222', '22', '05', '222', '0900000000')

#otp_info= EXEC_ACT(ORDER_API.queryCreditOTP, '0900000000')

#EXEC_ACT(ORDER_API.inputOTP, otp_info)

MERC_TID = order_info['MerchantTradeNo']
time.sleep(5)

#ExpressMap
MAP_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ExpressMap', CASE_NAME, 'OrderInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

map_req_info = EXEC_ACT(ACT_API.genOrderRequestInfo, MAP_INFO_CSV, MERC_TID)

EXEC_ACT(ACT_API.ExpressMapByBrowser, DRIVER, map_req_info)

#VERIFY
VERIFY(VER_API.verifyExpressFAMIMap, DRIVER)

time.sleep(5)
DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)