# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActCrossQueryLogisticsTradeInfo import actCrossQueryLogisticsTradeInfo
from ECpay.Verification.VerifyECpayAPI.VerifyCrossQueryLogisticsTradeInfo import verifyCrossQueryLogisticsTradeInfo


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
ACT_API = actCrossQueryLogisticsTradeInfo()
VER_API = verifyCrossQueryLogisticsTradeInfo()

#Testing exec
# precondition gen AIO order
# ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CrossQueryLogisticsTradeInfo', 'Initial_Data', 'AioCheckOut.csv')
#
# EXEC_ACT(ACT_API.enableWebOperate, DRIVER)
#
# order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)
#
# EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info, 'ChkoutEC_API')
#
# time.sleep(5)
#
# # precondition gen create cvs
#
# ORDER_INFO_CVS_CRT = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CrossQueryLogisticsTradeInfo', 'Initial_Data', 'Create.csv')
#
# order_info_crt = EXEC_ACT(ACT_API.genOrderRequestCreateCVS, ORDER_INFO_CVS_CRT, order_info['MerchantTradeNo'],
#                           order_info['MerchantTradeDate'])
#
# order_info_crt_res = EXEC_ACT(ACT_API.genPostRequestToApi, order_info_crt, 'Create_API')
#
# time.sleep(5)
# print order_info_crt_res
#
# modify_str = EXEC_ACT(ACT_API.modifyAllpaylogisticsSplit, order_info_crt_res)
# modify_data = EXEC_ACT(ACT_API.modifyAllpaylogisticsSplit, order_info_crt_res, True)
# print modify_str
# Do QueryLogisticsTradeInfo
QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CrossQueryLogisticsTradeInfo', CASE_NAME, 'OrderInfo.csv')

query_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2c, QUERY_INFO_CSV)

response = EXEC_ACT(ACT_API.genPostRequestToAPI, query_info)

order_info_res_dict = EXEC_ACT(ACT_API.strToDict, response)




data = EXEC_ACT(ACT_API.decryptDatab2c, order_info_res_dict['Data'])
print(data)


# VERIFY
#VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME, 'success')

VERIFY(VER_API.verifyResponseValuesb2c, CASE_NAME, data)
time.sleep(3)

#query_info = EXEC_ACT(ACT_API.genOrderRequestInfoWithALID, QUERY_INFO_CSV, modify_str)

# response = EXEC_ACT(ACT_API.genPostRequestToApi, query_info, 'QueryLogisticsTradeInfo_API')
#
# data = EXEC_ACT(ACT_API.strToDict, response)
#
# print data

# VERIFY(VER_API.verifyInfoReturn, data, CASE_NAME)

DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)