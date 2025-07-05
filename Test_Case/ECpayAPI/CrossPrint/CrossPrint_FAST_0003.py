# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActCrossPrint import actCrossPrint
from ECpay.Verification.VerifyECpayAPI.VerifyCrossPrint import verifyCrossPrint


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
ACT_API = actCrossPrint()
VER_API = verifyCrossPrint()

#Testing exec
# precondition gen AIO order


ORDER_INFO_CVS_CRT = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CrossPrint', 'Initial_Data', 'Create1.csv')


order_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2c, ORDER_INFO_CVS_CRT)

order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPICre, order_info)

order_info_res_dict = EXEC_ACT(ACT_API.strToDict, order_info_res)



data = EXEC_ACT(ACT_API.decryptDatab2c, order_info_res_dict['Data'])
print(data)





QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CrossPrint', CASE_NAME, 'OrderInfo.csv')

query_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2cLog, QUERY_INFO_CSV,data)

response = EXEC_ACT(ACT_API.genPostRequestToAPI, query_info)

order_info_res_dict1 = EXEC_ACT(ACT_API.strToDict, response)



data1 = EXEC_ACT(ACT_API.decryptDatab2c, order_info_res_dict1['Data'])

# VERIFY
#VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME, 'success')

VERIFY(VER_API.verifyResponseValuesb2c, CASE_NAME, data1)

time.sleep(4)



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