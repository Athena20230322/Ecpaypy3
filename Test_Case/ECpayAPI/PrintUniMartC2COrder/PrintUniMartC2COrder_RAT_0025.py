# -*- coding: utf-8 -*-


#Static Import Area
import argparse
import os
import time

from ECpay.Verification.VerifyECpayAPI.VerifyPrintUniMartC2COrder import verifyPrintUniMartC2COrder
from ECpay.ProdActions.ActECpayAPI.ActPrintUniMartC2COrder import actPrintUniMartC2COrder
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper

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
ACT_API = actPrintUniMartC2COrder()
VER_API = verifyPrintUniMartC2COrder()

#Testing exec

#Testing exec
#precondition add new order
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'PrintUniMartC2COrder', 'Initial_Data', 'OrderInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createAllpayOrderByBrowser, DRIVER, order_info)

#EXEC_ACT(ACT_API.inputPaymentPageCreditInfo, 'F128029956', '4311-9533-3333-3333', '22', '05', '222', '0900000000')

#otp_info= EXEC_ACT(ACT_API.queryCreditOTP, '0900000000')

#EXEC_ACT(ACT_API.inputOTP, otp_info)

MERC_TID = order_info['MerchantTradeNo']

MERC_T_DT = order_info['MerchantTradeDate']
time.sleep(5)

#precondition: generate C2C order
C2C_ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_data', 'ECpayAPI', 'PrintUniMartC2COrder', 'Initial_Data', 'Create.csv')

c2c_order_info = EXEC_ACT(ACT_API.genC2COrderRequestInfo, C2C_ORDER_INFO_CSV, MERC_TID, MERC_T_DT)

response_text = EXEC_ACT(ACT_API.createOrderByRequest, c2c_order_info)

params = EXEC_ACT(ACT_API.getParamsFromResponse, response_text)

#PrintUniMartC2COrderInfo api
PRINT_UNIMART_C2C_CSV = os.path.join(ROOTDIR, 'Test_data', 'ECpayAPI', 'PrintUniMartC2COrder', CASE_NAME, 'OrderInfo.csv')

print_c2c_order = EXEC_ACT(ACT_API.genPrintInfo, PRINT_UNIMART_C2C_CSV, params['logisticsID'],
                           params['CVSPaymentNo'], params['CVSValidationNo'])

EXEC_ACT(ACT_API.printC2C, DRIVER, print_c2c_order)

time.sleep(5)

EXEC_ACT(ACT_API.confirmPrint, DRIVER)

ele = EXEC_ACT(ACT_API.getPrintElementExist, DRIVER)

time.sleep(2)

DRIVER.delete_all_cookies()
DRIVER.quit()

#verify
VERIFY(VER_API.verifyExistance, ele)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)