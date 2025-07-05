# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActOpenIDLogin import actOpenIDLogin
from Allpay.Verification.VerifyAllpayAPI.VerifyOpenIDLogin import verifyOpenIDLogin


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
ACT_API = actOpenIDLogin()
VER_API = verifyOpenIDLogin()

#Testing exec

LOGIN_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'OpenIDLogin', CASE_NAME, 'Login.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

login_info = EXEC_ACT(ACT_API.genLoginRequestInfo, LOGIN_INFO_CSV)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, login_info)

EXEC_ACT(ACT_API.login, 'qaat0001', 'pw0001')

res_dict = EXEC_ACT(ACT_API.getResultFromBrowser)

# Verification
VERIFY(VER_API.verifyResponseValue, res_dict, CASE_NAME)

DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
