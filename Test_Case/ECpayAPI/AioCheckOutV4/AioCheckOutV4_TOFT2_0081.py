# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActAioCheckOutV4 import actAioCheckOutV4
from ECpay.Verification.VerifyECpayAPI.VerifyAioCheckOutV4 import verifyAioCheckOutV4


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
DRIVER = clsWebDriverHelper().initWebDriver(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actAioCheckOutV4()
VER_API = verifyAioCheckOutV4()

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'AioCheckOutV4', CASE_NAME, 'OrderInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info)

EXEC_ACT(ACT_API.inputPaymentPageCreditInfoE5, '4311-9544-4444-4444', '23', '05', '222', '0900000000','autotest123@gmail.com','test', 'divide')

# EXEC_ACT(ACT_API.inputOTP)

# otp_info = EXEC_ACT(ACT_API.queryCreditOTP, '0900000000')
#
# EXEC_ACT(ACT_API.inputOTP, otp_info)

MERC_TID = order_info['MerchantTradeNo']
MERC_UID = order_info['MerchantID']
time.sleep(5)

#VERIFY(VER_API.verifyPaymentReturn, MERC_TID, {'PayAmt':'100'})

VERIFY(VER_API.verifyPaymentReturn, MERC_TID, CASE_NAME)

DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
