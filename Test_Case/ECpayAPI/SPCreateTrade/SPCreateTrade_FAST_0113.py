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
DRIVER = clsWebDriverHelper().minitWebDriver(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actSPCreateTrade()
VER_API = verifySPCreateTrade()

#Testing exec

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'SPCreateTrade',CASE_NAME, 'OrderInfo.csv')

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

response = EXEC_ACT(ACT_API.createOrderByRequest, order_info)

data = EXEC_ACT(ACT_API.strToDict, response)

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

html_path = os.path.join(ROOTDIR, 'Tmp')

EXEC_ACT(ACT_API.makeHtmlFile, html_path, data, 'CREDIT', 'CREDIT')

EXEC_ACT(ACT_API.mobilesubmitinputPaymentInfo, '4311-9522-2222-2222', '23', '05', '222', '0900000000', 'sam')

EXEC_ACT(ACT_API.mobileinputOTP)

# otp_info = EXEC_ACT(ACT_API.queryCreditOTP, '0900000000')
#
# EXEC_ACT(ACT_API.inputOTP, otp_info)

res = EXEC_ACT(ACT_API.mobileGetResult)

print(res)


res_data = EXEC_ACT(ACT_API.strToDict, res)

print(res_data)
time.sleep(10)
VERIFY(VER_API.verifyPaymentReturn, res_data['MerchantTradeNo'], CASE_NAME)

EXEC_ACT(ACT_API.cleanHtmlTmp, html_path)

DRIVER.delete_all_cookies()
DRIVER.quit()

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
