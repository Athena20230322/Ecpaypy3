# -*- coding: utf-8 -*-


# Static Import Area
import argparse
import os
import time

from ECpay.ProdActions.ActECpayAPI.ActCreateTestDataV2 import actCreateTestDataV2
from ECpay.Verification.VerifyECpayAPI.VerifyCreateTestDataV2 import verifyCreateTestDataV2
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
# DRIVER = clsWebDriverHelper().initWebDriver(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actCreateTestDataV2()
VER_API = verifyCreateTestDataV2()

#Testing exec

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CreateTestDataV2', CASE_NAME, 'OrderInfo.csv')

order_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2c, ORDER_INFO_CSV)

order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, order_info)

order_info_res_dict = EXEC_ACT(ACT_API.strToDict, order_info_res)



# VERIFY
#VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME, 'success')

data = EXEC_ACT(ACT_API.decryptDatab2c, order_info_res_dict['Data'])
print(data)


# VERIFY
#VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME, 'success')

VERIFY(VER_API.verifyResponseValuesb2c, CASE_NAME, data)
time.sleep(3)

# VERIFY(VER_API.verifyColumn, order_info_res_dict, CASE_NAME)
#
# VERIFY(VER_API.verifyCreateTestDataCheck, order_info_res)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)