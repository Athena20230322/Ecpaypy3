# -*- coding: utf-8 -*-


#Static Import Area
import argparse
import os
import time

from ECpay.ProdActions.ActECpayAPI.ActReturnCVS import actReturnCVS
from ECpay.ProdActions.ActECpayAPI.ActLogisticsCheckAcct import actLogisticsCheckAcct
from ECpay.Verification.VerifyECpayAPI.VerifyLogisticsCheckAcct import verifyLogisticsCheckAcct
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper

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
ORDER_API = actReturnCVS()
ACT_API = actLogisticsCheckAcct()
VER_API = verifyLogisticsCheckAcct()

#Testing exec
#precondition add new order
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnCVS', 'Initial_Data', 'AioCheckOut.csv')

EXEC_ACT(ORDER_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ORDER_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ORDER_API.createOrderByBrowser, DRIVER, order_info, 'ChkoutAP_API')

time.sleep(5)

DRIVER.delete_all_cookies()
DRIVER.quit()

#precondition: generate CVS order
ORDER_INFO_CVS_CRT = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnCVS', 'Initial_Data', 'Create.csv')

order_info_crt = EXEC_ACT(ORDER_API.genOrderRequestCreateCVS, ORDER_INFO_CVS_CRT, order_info['MerchantTradeNo'],
                          order_info['MerchantTradeDate'])

order_info_crt_res = EXEC_ACT(ORDER_API.genpostRequestToAPI, order_info_crt,
                              'https://logistics-stage.ecpay.com.tw/Express/Create')

time.sleep(5)

#precondition: ReturnCVS
ORDER_INFO_C2C = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnCVS', 'ReturnCVS_RAT_0001', 'OrderInfo.csv')

modify_str = EXEC_ACT(ORDER_API.modifyAllpaylogisticsSplit, order_info_crt_res)

order_info_returncvs = EXEC_ACT(ORDER_API.genOrderRequestCVS, ORDER_INFO_C2C, modify_str)

print(order_info)
return_cvs = EXEC_ACT(ORDER_API.genpostRequestToAPI, order_info_returncvs,
                      'https://logistics-stage.ecpay.com.tw/express/ReturnCVS')
print(return_cvs)

#LogisticsCheckAccoount api
RTN_MERC_TID = EXEC_ACT(ACT_API.getRtnMerTID, return_cvs)

RTN_ORDER_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'LogisticsCheckAcct', CASE_NAME, 'OrderInfo.csv')

req_info = EXEC_ACT(ACT_API.genRtnRequestInfo, RTN_ORDER_CSV, RTN_MERC_TID)

response = EXEC_ACT(ACT_API.RtnGoodsByRequest, req_info)

#VERIFY
VERIFY(VER_API.verifyResponseExist, response)


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)