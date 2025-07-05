# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActCreditCardPeriodAction import actCreditCardPeriodAction
from ECpay.Verification.VerifyECpayAPI.VerifyCreditCardPeriodAction import verifyCreditCardPeriodAction
from ECpay.ProdActions.ActECpayAPI.ActCreditCardPeriodActionB import actCreditCardPeriodActionB
from ECpay.Verification.VerifyECpayAPI.VerifyCreditCardPeriodActionB import verifyCreditCardPeriodActionB



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
EXEC_ACT = HELPER.execTestAction
DRIVER = clsWebDriverHelper().initWebDriver(PKG)
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actCreditCardPeriodAction()
VER_API = verifyCreditCardPeriodAction()
ACT_API1 = actCreditCardPeriodActionB()
VER_API1 = verifyCreditCardPeriodActionB()

#Testing exec


ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CreditCardPeriodActionB', CASE_NAME, 'OrderInfo3.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfoPID, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info)

EXEC_ACT(ACT_API.inputPaymentPageCreditInfoE, '4311-9544-4444-4444', '23', '05', '222', '0900000000','autotest123@gmail.com','test', 'divide')

EXEC_ACT(ACT_API.inputOTP)

MERC_TID = order_info['MerchantTradeNo']
MERC_UID = order_info['MerchantID']
time.sleep(5)


ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CreditCardPeriodActionB', CASE_NAME, 'OrderInfo2.csv')

order_info = EXEC_ACT(ACT_API1.genOrderRequestInfoPID, ORDER_INFO_CSV,MERC_TID)

#res = EXEC_ACT(ACT_API.createOrderByRequestThreeD, order_info)

order_info_res = EXEC_ACT(ACT_API1.genPostRequestToAPI, order_info)

res_dict = EXEC_ACT(ACT_API1.strToDict3D, order_info_res)

data = EXEC_ACT(ACT_API1.decryptData3DPID, res_dict['Data'])
print(data)

VERIFY(VER_API1.verifyResponseValuesThreeD, CASE_NAME, res_dict, data)




# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)