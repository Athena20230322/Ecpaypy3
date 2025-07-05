# -*- coding: utf-8 -*-


# Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

# Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActCapture import actCapture
from ECpay.Verification.VerifyECpayAPI.VerifyCapture import verifyCapture

# (DO NO Edit) Static declare
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
ACT_API = actCapture()
VER_API = verifyCapture()

# Testing exec

# Precondition-Create order
CREATE_ORDER_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'Capture', 'Initial_Data', 'CreateOrderInfoWithPlatform.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

create_order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, CREATE_ORDER_CSV)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, create_order_info)

EXEC_ACT(ACT_API.payMoney)

time.sleep(5)

# Capture
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'Capture', CASE_NAME, 'Capture.csv')

order_info = EXEC_ACT(ACT_API.genCaptureRequestInfo, ORDER_INFO_CSV, create_order_info['MerchantTradeNo'])

result_str = EXEC_ACT(ACT_API.captureResult, order_info)

result_dict = EXEC_ACT(ACT_API.strToDict, result_str)

platform_fee = EXEC_ACT(ACT_API.queryCaptureResult, DRIVER, 'qaat0001', 'pw0001', create_order_info['MerchantTradeNo'])

# VERIFY
VERIFY(VER_API.verifyCaptureInfo, order_info, result_dict, CASE_NAME)

VERIFY(VER_API.verifyPlatformCharge, order_info, platform_fee)

DRIVER.delete_all_cookies()
DRIVER.quit()

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
