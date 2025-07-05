# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActBindAccount import actBindAccount
from Allpay.ProdActions.ActAllpayAPI.ActRemoveMemberInfo import actRemoveMemberInfo
from Allpay.Verification.VerifyAllpayAPI.VerifyRemoveMemberInfo import verifyRemoveMemberInfo


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
BIND_API = actBindAccount()
ACT_API = actRemoveMemberInfo()
VER_API = verifyRemoveMemberInfo()

# precondition-BindAccount
BIND_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'RemoveMemberInfo', 'Initial_Data', 'BindAccount.csv')

EXEC_ACT(BIND_API.enableWebOperate, DRIVER)

bind_info, ID = EXEC_ACT(BIND_API.genBindInfo, BIND_INFO_CSV, 'person')

EXEC_ACT(BIND_API.createBindingByBrowser, DRIVER, bind_info)

EXEC_ACT(BIND_API.fillInLoginInfo, DRIVER, 'buyer0001', 'pw0001')

time.sleep(3)

# RemoveMemberInfo
REMOVE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'RemoveMemberInfo', CASE_NAME, 'Remove.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

remove_info = EXEC_ACT(ACT_API.genRemoveInfo, REMOVE_INFO_CSV, ID)

EXEC_ACT(ACT_API.createRemovingByBrowser, DRIVER, remove_info)

EXEC_ACT(ACT_API.fillInLoginInfo, DRIVER, 'buyer0001', 'pw0001')

remove_return = EXEC_ACT(ACT_API.getDataFromBrowser, DRIVER)

res_dict = EXEC_ACT(ACT_API.strToDict, remove_return)

platform_data = EXEC_ACT(ACT_API.decodeResult, res_dict)

# Verify
VERIFY(VER_API.verifyColumnNames, res_dict, platform_data, CASE_NAME)


DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
