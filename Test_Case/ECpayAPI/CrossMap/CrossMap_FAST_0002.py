# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActCrossMap import actCrossMap
from ECpay.Verification.VerifyECpayAPI.VerifyCrossMap import verifyCrossMap


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
ACT_API = actCrossMap()
VER_API = verifyCrossMap()

#Testing exec
#precondition add new order
print(ROOTDIR)
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CrossMap', 'Initial_Data', 'OrderInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderInfo, ORDER_INFO_CSV)

# EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info)

MERC_T_NO = order_info['MerchantTradeNo']
time.sleep(3)

#ExpressMap
MAP_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CrossMap', CASE_NAME, 'OrderInfo.csv')

map_req_info = EXEC_ACT(ACT_API.genOrderRequestInfo, MAP_INFO_CSV, MERC_T_NO)

EXEC_ACT(ACT_API.CrossMapByBrowser, DRIVER, map_req_info)

time.sleep(2)

EXEC_ACT(ACT_API.ChooseCrossLog)

time.sleep(3)

DRIVER.delete_all_cookies()
DRIVER.quit()

response = EXEC_ACT(ACT_API.GetInfoFromServerReplyUrl, MERC_T_NO)



# data = EXEC_ACT(ACT_API.decryptDatab2c, order_info_res_dict['Data'])
# print data


# VERIFY
#VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME, 'success')

# VERIFY(VER_API.verifyResponseValuesb2c, CASE_NAME, data)
# time.sleep(3)

#VERIFY
#VERIFY(VER_API.verifyCrossReturnResult, response, map_req_info)




# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)