# -*- coding: utf-8 -*-


#Static Import Area
import argparse
import os
import time

from ECpay.ProdActions.ActECpayAPI.ActCancelC2COrder import actCancelC2COrder
from ECpay.Verification.VerifyECpayAPI.VerifyCancelC2COrder import verifyCancelC2COrder
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper

#(DO NO Edit) Static declare

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
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances

ACT_API = actCancelC2COrder()
VER_API = verifyCancelC2COrder()

# Testing exec

# Precondition create ECPay new order info

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CancelC2COrder', 'Initial_Data', 'AioCheckOut.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info, 'ChkoutEC_API')

time.sleep(3)

# Precondition create logistics order info

ORDER_INFO_CVS_CRT = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CancelC2COrder', 'Initial_Data', 'Create.csv')

order_info_crt = EXEC_ACT(ACT_API.genOrderRequestCreate, ORDER_INFO_CVS_CRT, order_info['MerchantTradeNo'],
                          order_info['MerchantTradeDate'])

order_info_crt_res = EXEC_ACT(ACT_API.genpostRequestToAPI, order_info_crt, 'Create_API')

# Do CancelC2COrder_API

ORDER_INFO_C2C = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'CancelC2COrder', CASE_NAME, 'OrderInfo.csv')

EXEC_ACT(VER_API.enableWebOperate, DRIVER)

modify_str = EXEC_ACT(ACT_API.modifyAllpaylogisticsSplit, order_info_crt_res)

order_info_cancel_c2c = EXEC_ACT(ACT_API.genOrderRequestC2C, ORDER_INFO_C2C, modify_str, "' or 1=1 /*")

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info_cancel_c2c, 'Cancel_C2C_API')

VERIFY(VER_API.verifyStatusResult, '0|無相關訂單可提供取消。')

DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)