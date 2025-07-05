# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActprintTradeDocumentV2 import actprintTradeDocumentV2
from ECpay.Verification.VerifyECpayAPI.VerifyprintTradeDocumentV2 import verifyprintTradeDocumentV2


from ECpay.ProdActions.ActECpayAPI.ActCreateByTempTradeV2 import actCreateByTempTradeV2
from ECpay.Verification.VerifyECpayAPI.VerifyCreateByTempTradeV2 import verifyCreateByTempTradeV2

from ECpay.ProdActions.ActECpayAPI.ActCreateV2 import actCreateV2
from ECpay.Verification.VerifyECpayAPI.VerifyCreateV2 import verifyCreateV2

#from ECpay.ProdActions.ActECpayAPI.ActCrossPrint import actCrossPrint
#from ECpay.Verification.VerifyECpayAPI.VerifyCrossPrint import verifyCrossPrint

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


ACT_API1 = actCreateV2()
VER_API1 = verifyCreateV2()
ACT_API2 = actCreateByTempTradeV2()
VER_API2 = verifyCreateByTempTradeV2()
#ACT_API = actCrossPrint()
#VER_API = verifyCrossPrint()
ACT_API = actprintTradeDocumentV2()
VER_API = verifyprintTradeDocumentV2()

#Testing exec
# precondition gen AIO order


ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CreateV2', CASE_NAME, 'OrderInfo.csv')



EXEC_ACT(ACT_API1.enableWebOperate, DRIVER)

#order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI1, order_info)
EXEC_ACT(ACT_API1.createOrderByBrowser132)
time.sleep(5)
response = EXEC_ACT(ACT_API1.submitLogisticsRequestFAM)


res_in_CliReUrl = EXEC_ACT(ACT_API1.GetInfoFromClientRedirectUrl)

res_in_CliReUrl_dict = EXEC_ACT(ACT_API1.strToDict1, res_in_CliReUrl)

print(res_in_CliReUrl_dict)

print("4234125")



ORDER_INFO_CVS_CRT = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CreateByTempTradeV2', 'Initial_Data', 'Create1.csv')


order_info = EXEC_ACT(ACT_API2.genOrderRequestInfoB2cPritnTrade, ORDER_INFO_CVS_CRT,res_in_CliReUrl_dict)

order_info_res = EXEC_ACT(ACT_API2.genPostRequestToAPICre, order_info)


order_info_res_dict = EXEC_ACT(ACT_API2.strToDict, order_info_res)


data = EXEC_ACT(ACT_API.decryptDatab2c, order_info_res_dict['Data'])
print(data)





EXEC_ACT(ACT_API.enableWebOperate, DRIVER)
QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'printTradeDocumentV2', CASE_NAME, 'OrderInfo.csv')

query_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2cLog, QUERY_INFO_CSV,data)

html_path = os.path.join(ROOTDIR, 'Tmp')

response = EXEC_ACT(ACT_API.genPostRequestToAPI, query_info,html_path)


#order_info_res_dict1 = EXEC_ACT(ACT_API.strToDictP, response)



#data1 = EXEC_ACT(ACT_API.decryptDatab2c, order_info_res_dict1['Data'])

# VERIFY
#VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME, 'success')

#VERIFY(VER_API.verifyResponseValuesb2c, CASE_NAME, data1)

time.sleep(4)
EXEC_ACT(ACT_API.cleanHtmlTmp, html_path)



DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)