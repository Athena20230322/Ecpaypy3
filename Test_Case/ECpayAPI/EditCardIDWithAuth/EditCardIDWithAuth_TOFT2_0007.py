# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActEditCardIDWithAuth import actEditCardIDWithAuth
from ECpay.Verification.VerifyECpayAPI.VerifyEditCardIDWithAuth import verifyEditCardIDWithAuth


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
ACT_API = actEditCardIDWithAuth()
VER_API = verifyEditCardIDWithAuth()

# Testing exec

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'EditCardIDWithAuth', CASE_NAME, 'OrderInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info)

EXEC_ACT(ACT_API.inputOldCreditCard4NoInfo, '4444')

EXEC_ACT(ACT_API.inputEditCreditCardInfo, '4311-9544-4444-4444', '222')

response = EXEC_ACT(ACT_API.GetInfoFromServerReplyUrl, order_info['MerchantTradeNo'])

client_text = EXEC_ACT(ACT_API.GetInfoFromClientRedirectUrl)

client_dict = EXEC_ACT(ACT_API.redirectStrToDict, client_text)

# VERIFY
VERIFY(VER_API.verifyServerReplyColumnsCheck, response, CASE_NAME, order_info['MerchantTradeNo'])

VERIFY(VER_API.verifyClientRedirectColumnsCheck, client_dict, CASE_NAME, order_info['MerchantTradeNo'])

DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)