# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActBindAccount import actBindAccount
from Allpay.Verification.VerifyAllpayAPI.VerifyBindAccount import verifyBindAccount


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
ACT_API = actBindAccount()
VER_API = verifyBindAccount()

#Testing exec

BIND_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'BindAccount', CASE_NAME, 'BindAccount.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

bind_info, ID = EXEC_ACT(ACT_API.genBindInfo, BIND_INFO_CSV, 'company')

EXEC_ACT(ACT_API.createBindingByBrowser, DRIVER, bind_info)

EXEC_ACT(ACT_API.fillInLoginInfo, DRIVER, 'company0001', 'pw0001')

bind_account_return = EXEC_ACT(ACT_API.getDataFromBrowser, DRIVER)

res_dict = EXEC_ACT(ACT_API.decodeResult, bind_account_return)

# Verification
print(bind_info)
VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME, ID)

DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
