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
# DRIVER = clsWebDriverHelper().initWebDriver(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actReturnUniMartCVS()
VER_API = verifyReturnUniMartCVS()

#Testing exec

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnUniMartCVS', 'Initial_Data', 'UniMartTestData.csv')

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

order_info_crt_res = EXEC_ACT(ACT_API.genPostRequestToApi, order_info, 'CreateTest_API')

# ReturnUniMartCVS

ORDER_RETURN_CVS = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnUniMartCVS', CASE_NAME, 'OrderInfo.csv')

modify_str = EXEC_ACT(ACT_API.modifyAllpaylogisticsSplit, order_info_crt_res)

order_info_returnunimartcvs = EXEC_ACT(ACT_API.genOrderRequestCVS, ORDER_RETURN_CVS, modify_str, True, True)

response = EXEC_ACT(ACT_API.genPostRequestToApi, order_info_returnunimartcvs, 'ReturnUniMartCVS_API')

VERIFY(VER_API.verifyReturnCVSStrResult, response)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
