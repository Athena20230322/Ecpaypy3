# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from  Allpay.ProdActions.ActAllpayAPI.ActAioCheckOut import actAioCheckOut
from Allpay.Verification.VerifyAPI.VerifyAioCheckOut import verifyAioCheckOut


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
ACT_API = actAioCheckOut()
VER_API = verifyAioCheckOut()

#Testing exec

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'AioCheckOut', CASE_NAME, 'OrderInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info)

EXEC_ACT(ACT_API.inputPaymentPageCreditInfo, '4311-9533-3333-3333', '22', '05', '222', '0963957452')

otp_info= EXEC_ACT(ACT_API.queryCreditOTP, '0963957452')

EXEC_ACT(ACT_API.inputOTP, otp_info)

MERC_TID = order_info['MerchantTradeNo']
time.sleep(5)
#VERIFY(VER_API.verifyPaymentReturn, MERC_TID, {'PayAmt':'100'})

VERIFY(VER_API.verifyPaymentReturn, MERC_TID, CASE_NAME)

#VER_API.verifyPaymentReturn(MERC_TID, CASE_NAME)

DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)