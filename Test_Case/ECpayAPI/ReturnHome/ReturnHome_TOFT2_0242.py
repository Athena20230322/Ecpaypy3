# -*- coding: utf-8 -*-


#Static Import Area
import argparse
import os

from  ECpay.ProdActions.ActECpayAPI.ActReturnHome import actReturnHome
from ECpay.Verification.VerifyECpayAPI.VerifyReturnHome import verifyReturnHome
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
# DRIVER = clsWebDriverHelper().initWebDriver(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actReturnHome()
VER_API = verifyReturnHome()

# Testing exec

ORDER_INFO_CVS_C2C = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'ReturnHome', CASE_NAME, 'OrderInfo.csv')

order_info_home = EXEC_ACT(ACT_API.genOrderRequestCVS, ORDER_INFO_CVS_C2C, '')

order_info_rehome_res = EXEC_ACT(ACT_API.genpostRequestToAPI, order_info_home, 'ReHome_API')

VERIFY(VER_API.verifyReturnHomeCVSResult, order_info_rehome_res)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)