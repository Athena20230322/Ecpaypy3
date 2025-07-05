# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActQueryLogisticsTradeInfo import actQueryLogisticsTradeInfo
from ECpay.Verification.VerifyECpayAPI.VerifyQueryLogisticsTradeInfo import verifyQueryLogisticsTradeInfo


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
ACT_API = actQueryLogisticsTradeInfo()
VER_API = verifyQueryLogisticsTradeInfo()

#Testing exec
# precondition gen AIO order
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'QueryLogisticsTradeInfo', 'Initial_Data', 'AioCheckOut.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info, 'ChkoutEC_API')

time.sleep(5)

# precondition gen create cvs

ORDER_INFO_CVS_CRT = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'QueryLogisticsTradeInfo', 'Initial_Data', 'Create.csv')

order_info_crt = EXEC_ACT(ACT_API.genOrderRequestCreateCVS, ORDER_INFO_CVS_CRT, order_info['MerchantTradeNo'],
                          order_info['MerchantTradeDate'])

order_info_crt_res = EXEC_ACT(ACT_API.genPostRequestToApi, order_info_crt, 'Create_API')

time.sleep(5)
print(order_info_crt_res)

modify_str = EXEC_ACT(ACT_API.modifyAllpaylogisticsSplit, order_info_crt_res)
modify_data = EXEC_ACT(ACT_API.modifyAllpaylogisticsSplit, order_info_crt_res, True)
print(modify_str)
# Do QueryLogisticsTradeInfo
QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'QueryLogisticsTradeInfo', CASE_NAME, 'OrderInfo.csv')

query_info = EXEC_ACT(ACT_API.genOrderRequestInfoWithALID, QUERY_INFO_CSV, modify_str)

response = EXEC_ACT(ACT_API.genPostRequestToApi, query_info, 'QueryLogisticsTradeInfo_API')

data = EXEC_ACT(ACT_API.strToDict, response)

print(data)

VERIFY(VER_API.verifyInfoReturn, data, CASE_NAME, modify_str, order_info['MerchantTradeNo'], data['ShipmentNo'],
       modify_data['BookingNote'])

DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)