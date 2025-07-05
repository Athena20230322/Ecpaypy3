# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActReturnUniMartCVS import actReturnUniMartCVS
from ECpay.Verification.VerifyECpayAPI.VerifyReturnUniMartCVS import verifyReturnUniMartCVS


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
ACT_API = actReturnUniMartCVS()
VER_API = verifyReturnUniMartCVS()

#Testing exec
# precondition create order
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnUniMartCVS', 'Initial_Data', 'AioCheckOut.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)
EXEC_ACT(VER_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info, 'ChkoutEC_API')

time.sleep(3)

# precondition gen create cvs

ORDER_INFO_CVS_CRT = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnUniMartCVS', 'Initial_Data', 'Create.csv')

order_info_crt = EXEC_ACT(ACT_API.genOrderRequestCreateCVS, ORDER_INFO_CVS_CRT, order_info['MerchantTradeNo'],
                          order_info['MerchantTradeDate'])

order_info_crt_res = EXEC_ACT(ACT_API.genPostRequestToApi, order_info_crt, 'Create_API')

time.sleep(3)

ORDER_RETURN_CVS = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnUniMartCVS', CASE_NAME, 'OrderInfo.csv')

modify_str = EXEC_ACT(ACT_API.modifyAllpaylogisticsSplit, order_info_crt_res)

print(modify_str)

order_returncvs = EXEC_ACT(ACT_API.genOrderRequestCVS, ORDER_RETURN_CVS, modify_str, False, False)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_returncvs, 'ReturnUniMartCVS_API')

server_response = EXEC_ACT(ACT_API.GetInfoFromServerReplyUrl, modify_str)

VERIFY(VER_API.verifyServerReplyValues, server_response, CASE_NAME)

VERIFY(VER_API.verifyReturnCVSResult)

DRIVER.delete_all_cookies()
DRIVER.quit()

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
