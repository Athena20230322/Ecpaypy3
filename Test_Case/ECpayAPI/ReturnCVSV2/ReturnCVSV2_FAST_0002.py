# -*- coding: utf-8 -*-


# Static Import Area
import argparse
import os
import time

from ECpay.ProdActions.ActECpayAPI.ActReturnCVSV2 import actReturnCVSV2
from ECpay.Verification.VerifyECpayAPI.VerifyReturnCVSV2 import verifyReturnCVSV2
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper

#from ECpay.ProdActions.ActECpayAPI.ActCreateByTempTrade import actCreateByTempTrade
#from ECpay.Verification.VerifyECpayAPI.VerifyCreateByTempTrade import verifyCreateByTempTrade

from ECpay.ProdActions.ActECpayAPI.ActCreateV2 import actCreateV2
from ECpay.Verification.VerifyECpayAPI.VerifyCreateV2 import verifyCreateV2

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
ACT_API2 = actReturnCVSV2()
VER_API2 = verifyReturnCVSV2()
#ACT_API1 = actCreateV2()
#VER_API1 = verifyCreateV2()
#ACT_API = actCreateByTempTrade()
#VER_API = verifyCreateByTempTrade()



#ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CreateV2', CASE_NAME, 'OrderInfo.csv')



#EXEC_ACT(ACT_API1.enableWebOperate, DRIVER)

#order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI1, order_info)
#EXEC_ACT(ACT_API1.createOrderByBrowser)
#time.sleep(5)
#response = EXEC_ACT(ACT_API1.submitLogisticsRequestFAM)


#res_in_CliReUrl = EXEC_ACT(ACT_API1.GetInfoFromClientRedirectUrl)

#res_in_CliReUrl_dict = EXEC_ACT(ACT_API1.strToDict, res_in_CliReUrl)






#ORDER_INFO_CVS_CRT = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CreateByTempTrade', 'Initial_Data', 'Create.csv')


#order_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2c, ORDER_INFO_CVS_CRT,res_in_CliReUrl_dict)

#order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPICre, order_info)

#order_info_res_dict = EXEC_ACT(ACT_API.strToDict, order_info_res)



#data = EXEC_ACT(ACT_API.decryptDatab2c, order_info_res_dict['Data'])
#print data



#Testing exec
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnCVSV2', CASE_NAME, 'OrderInfo.csv')


order_info = EXEC_ACT(ACT_API2.genOrderRequestInfoB2cCSV2, ORDER_INFO_CSV)

order_info_res = EXEC_ACT(ACT_API2.genPostRequestToAPI, order_info)

order_info_res_dict = EXEC_ACT(ACT_API2.strToDict, order_info_res)

time.sleep(5)

# VERIFY
#VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME, 'success')

data = EXEC_ACT(ACT_API2.decryptDatab2c, order_info_res_dict['Data'])
print(data)







# VERIFY
#VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME, 'success')

VERIFY(VER_API2.verifyResponseValuesb2c, CASE_NAME, data)
time.sleep(5)

# VERIFY(VER_API.verifyColumn, order_info_res_dict, CASE_NAME)
#
# VERIFY(VER_API.verifyCreateTestDataCheck, order_info_res)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)