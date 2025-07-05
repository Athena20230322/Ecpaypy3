# -*- coding: utf-8 -*-


#Static Import Area


from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActCreditCardPeriodAction import actCreditCardPeriodAction
from ECpay.Verification.VerifyECpayAPI.VerifyCreditCardPeriodAction import verifyCreditCardPeriodAction





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
ROOTDIR = HELPER.rootdir
DRIVER = clsWebDriverHelper().initWebDriver(PKG)
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actCreditCardPeriodAction()
VER_API = verifyCreditCardPeriodAction()



#Testing exec

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CreditCardPeriodAction', CASE_NAME, 'OrderInfo3.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfoPID, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info)

EXEC_ACT(ACT_API.inputPaymentPageCreditInfoE, '4311-9544-4444-4444', '23', '05', '222', '0900000000','autotest123@gmail.com','test', 'divide')

EXEC_ACT(ACT_API.inputOTP)

MERC_TID = order_info['MerchantTradeNo']
MERC_UID = order_info['MerchantID']
time.sleep(5)



QUERY_TRADE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CreditCardPeriodAction', CASE_NAME, 'OrderInfo2.csv')

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo2, QUERY_TRADE_INFO_CSV,MERC_TID)


order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, order_info)

res_dict = EXEC_ACT(ACT_API.strToDict, order_info_res)

VERIFY(VER_API.verifyInfoReturn, res_dict, CASE_NAME)




# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)