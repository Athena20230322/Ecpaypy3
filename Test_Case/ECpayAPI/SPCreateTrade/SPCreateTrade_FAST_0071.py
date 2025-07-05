# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActSPCreateTrade import actSPCreateTrade
from ECpay.Verification.VerifyECpayAPI.VerifySPCreateTrade import verifySPCreateTrade


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
ACT_API = actSPCreateTrade()
VER_API = verifySPCreateTrade()

#Testing exec

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'SPCreateTrade', 'SPCreateTrade_FAST_0071', 'OrderInfo.csv')

order_info = EXEC_ACT(ACT_API.genOrderRequestInfoPID, ORDER_INFO_CSV)


response = EXEC_ACT(ACT_API.createOrderByRequest, order_info)

data = EXEC_ACT(ACT_API.strToDict, response)

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

html_path = os.path.join(ROOTDIR, 'Tmp')

EXEC_ACT(ACT_API.makeHtmlFile, html_path, data, 'CREDIT', 'CREDIT')

time.sleep(10)

EXEC_ACT(ACT_API.inputPaymentPageCreditInfoBind, '4311-9544-4444-4444', '23', '05', '222', '0900000000', 'Test', 'divide', True)


#EXEC_ACT(ACT_API.inputOTP)

# otp_info = EXEC_ACT(ACT_API.queryCreditOTP, '0900000000')
#
# EXEC_ACT(ACT_API.inputOTP, otp_info)




EXEC_ACT(ACT_API.inputOTP)

MERC_TID = order_info['MerchantTradeNo']
MERC_UID = order_info['MerchantID']


EXEC_ACT(ACT_API.cleanHtmlTmp, html_path)

DRIVER.delete_all_cookies()
DRIVER.quit()

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
