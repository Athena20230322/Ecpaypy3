# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActPrintOKC2COrder import actPrintOKC2COrder
from ECpay.Verification.VerifyECpayAPI.VerifyPrintOKC2COrder import verifyPrintOKC2COrder


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
DRIVER = clsWebDriverHelper().initWebDriverHilife(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actPrintOKC2COrder()
VER_API = verifyPrintOKC2COrder()

#Testing exec
#precondition add new order
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'PrintOKC2COrder', 'Initial_Data', 'OrderInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createECpayOrderByBrowser, DRIVER, order_info)

#EXEC_ACT(ACT_API.inputPaymentPageCreditInfo, 'F128029956', '4311-9533-3333-3333', '22', '05', '222', '0900000000')

#otp_info= EXEC_ACT(ACT_API.queryCreditOTP, '0900000000')

#EXEC_ACT(ACT_API.inputOTP, otp_info)

MERC_TID = order_info['MerchantTradeNo']

MERC_T_DT = order_info['MerchantTradeDate']
time.sleep(3)

#precondition: generate C2C order
C2C_ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_data', 'ECpayAPI', 'PrintOKC2COrder', 'Initial_Data', 'Create.csv')

c2c_order_info = EXEC_ACT(ACT_API.genC2COrderRequestInfo, C2C_ORDER_INFO_CSV, MERC_TID, MERC_T_DT)

response_text = EXEC_ACT(ACT_API.createOrderByRequest, c2c_order_info)

params = EXEC_ACT(ACT_API.getParamsFromResponse, response_text)

#PrintHILIFEC2COrderInfo api
PRINT_HILIFE_C2C_CSV = os.path.join(ROOTDIR, 'Test_data', 'ECpayAPI', 'PrintOKC2COrder', CASE_NAME, 'OrderInfo.csv')

print_c2c_order_info = EXEC_ACT(ACT_API.genPrintInfo, PRINT_HILIFE_C2C_CSV, params['logisticsID'], params['CVSPaymentNo'])

EXEC_ACT(ACT_API.printC2C, DRIVER, print_c2c_order_info)

time.sleep(2)

ele = EXEC_ACT(ACT_API.getPrintElements)


#VERIFY
#VERIFY(VER_API.verifyPrintInfo, print_c2c_order_info, ele, c2c_order_info['SenderName'], c2c_order_info['ReceiverName'])

DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
