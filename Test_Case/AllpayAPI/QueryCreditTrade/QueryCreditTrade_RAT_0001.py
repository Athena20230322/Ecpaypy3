# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActLoginPage import actLoginPage
from Allpay.ProdActions.ActAllpayAPI.ActQueryCreditTrade import actQueryCreditTrade
from Allpay.Verification.VerifyAllpayAPI.VerifyQueryCreditTrade import verifyQueryCreditTrade


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
LOG_API = actLoginPage(DRIVER, SUM_LOG)
ACT_API = actQueryCreditTrade()
VER_API = verifyQueryCreditTrade()

#Testing exec
#Precondition-Create order
CREATE_ORDER_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'QueryCreditTrade', 'Initial_Data'
                                , 'CreateOrderInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

EXEC_ACT(LOG_API.generalLogin, 'test0001', 'pw0001')

create_order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, CREATE_ORDER_CSV)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, create_order_info)

EXEC_ACT(ACT_API.inputPaymentPageCreditInfo, 'F128029956', '4311-9522-2222-2222', '22', '05', '222', '0911429215')

EXEC_ACT(ACT_API.confirmSubmitCreditInfo, DRIVER)

EXEC_ACT(ACT_API.confirmOrderSuccess)

#QueryCreditTrade
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'QueryCreditTrade', CASE_NAME, 'OrderInfo.csv')

order_info = EXEC_ACT(ACT_API.genQueryRequestInfo, ORDER_INFO_CSV, create_order_info['MerchantTradeNo'])

response_json = EXEC_ACT(ACT_API.queryCreditCardPeriodInfo, order_info)

#VERIFY
VERIFY(VER_API.verifyResponseColumnName, response_json, CASE_NAME)

DRIVER.delete_all_cookies()
DRIVER.quit()

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
