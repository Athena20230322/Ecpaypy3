# -*- coding: utf-8 -*-


# Static Import Area
import argparse
import os
import time

from ECpay.ProdActions.ActECpayAPI.ActCreateV2 import actCreateV2
from ECpay.Verification.VerifyECpayAPI.VerifyCreateV2 import verifyCreateV2


from ECpay.ProdActions.ActECpayAPI.ActCreateByTempTradeV2 import actCreateByTempTradeV2
from ECpay.Verification.VerifyECpayAPI.VerifyCreateByTempTradeV2 import verifyCreateByTempTradeV2

from ECpay.ProdActions.ActECpayAPI.ActQueryLogisticsTradeInfoV2 import actQueryLogisticsTradeInfoV2
from ECpay.Verification.VerifyECpayAPI.VerifyQueryLogisticsTradeInfoV2 import verifyQueryLogisticsTradeInfoV2

from ECpay.ProdActions.ActECpayAPI.ActUpdateStoreInfoV2 import actUpdateStoreInfoV2
from ECpay.Verification.VerifyECpayAPI.VerifyUpdateStoreInfoV2 import verifyUpdateStoreInfoV2



from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper

# (DO NO Edit) Static declare

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
# DRIVER = clsWebDriverHelper().initWebDriver(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances

ACT_API1 = actCreateV2()
VER_API1 = verifyCreateV2()

ACT_API2 = actCreateByTempTradeV2()
VER_API2 = verifyCreateByTempTradeV2()

ACT_API3 = actQueryLogisticsTradeInfoV2()
VER_API3 = verifyQueryLogisticsTradeInfoV2()



ACT_API = actUpdateStoreInfoV2()
VER_API = verifyUpdateStoreInfoV2()

#Testing exec



EXEC_ACT(ACT_API1.enableWebOperate, DRIVER)

#order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI1, order_info)
EXEC_ACT(ACT_API1.createOrderByBrowser)
time.sleep(5)
response = EXEC_ACT(ACT_API1.submitLogisticsRequestFAM)


res_in_CliReUrl = EXEC_ACT(ACT_API1.GetInfoFromClientRedirectUrl)

res_in_CliReUrl_dict = EXEC_ACT(ACT_API1.strToDict1, res_in_CliReUrl)

print(res_in_CliReUrl_dict)


ORDER_INFO_CVS_CRT = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CreateByTempTradeV2', 'Initial_Data', 'Create.csv')


order_info = EXEC_ACT(ACT_API2.genOrderRequestInfoB2cCreateBy, ORDER_INFO_CVS_CRT,res_in_CliReUrl_dict)

order_info_res = EXEC_ACT(ACT_API2.genPostRequestToAPICre, order_info)


order_info_res_dict = EXEC_ACT(ACT_API2.strToDict, order_info_res)


data = EXEC_ACT(ACT_API2.decryptDatab2c, order_info_res_dict['Data'])
print(data)




QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'QueryLogisticsTradeInfoV2', 'QueryLogisticsTradeInfoV2_TOFT2_0005', 'OrderInfo.csv')

query_info = EXEC_ACT(ACT_API3.genOrderRequestInfoB2cQuery, QUERY_INFO_CSV,data)

response = EXEC_ACT(ACT_API3.genPostRequestToAPI, query_info)

order_info_res_dict = EXEC_ACT(ACT_API3.strToDict, response)




data1 = EXEC_ACT(ACT_API3.decryptDatab2c, order_info_res_dict['Data'])
print(data1)




#order_info_crt_res = EXEC_ACT(ACT_API.genpostRequestToAPI, order_info_crt, 'Create_API')


ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'UpdateStoreInfoV2', CASE_NAME, 'UpdateStoreInfoV2.csv')

order_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2cUpdateStoreV2FH, ORDER_INFO_CSV,data1)

order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, order_info)

order_info_res_dict = EXEC_ACT(ACT_API.strToDict, order_info_res)



# VERIFY
#VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME, 'success')

data2 = EXEC_ACT(ACT_API.decryptDatab2c, order_info_res_dict['Data'])
print(data2)


# VERIFY
#VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME, 'success')

VERIFY(VER_API.verifyResponseValuesb2c, CASE_NAME, data2)
time.sleep(3)

# VERIFY(VER_API.verifyColumn, order_info_res_dict, CASE_NAME)
#
# VERIFY(VER_API.verifyCreateTestDataCheck, order_info_res)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)