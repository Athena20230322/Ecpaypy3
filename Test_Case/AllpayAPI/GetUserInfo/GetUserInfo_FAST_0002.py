# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActGetUserInfo import actGetUserInfo
from Allpay.Verification.VerifyAllpayAPI.VerifyGetUserInfo import verifyGetUserInfo
from Allpay.ProdActions.ActAllpayAPI.ActOpenIDLogin import actOpenIDLogin
from Allpay.Verification.VerifyAllpayAPI.VerifyOpenIDLogin import verifyOpenIDLogin


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
ACT_OL_API = actOpenIDLogin()
VER_OL_API = verifyOpenIDLogin()
ACT_API = actGetUserInfo()
VER_API = verifyGetUserInfo()

# Precondition OpenIDLogin
LOGIN_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'OpenIDLogin', 'OpenIDLogin_RAT_0001', 'Login.csv')

EXEC_ACT(ACT_OL_API.enableWebOperate, DRIVER)

login_info = EXEC_ACT(ACT_OL_API.genLoginRequestInfo, LOGIN_INFO_CSV)

EXEC_ACT(ACT_OL_API.createOrderByBrowser, DRIVER, login_info)

EXEC_ACT(ACT_OL_API.login, 'qaat0001', 'pw0001')

res_dict = EXEC_ACT(ACT_OL_API.getResultFromBrowser)

# Precondition OpenIDLogin verification

VERIFY(VER_OL_API.verifyColumnNames, res_dict, 'OpenIDLogin_RAT_0001')

# Testing exec

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'GetUserInfo', CASE_NAME, 'OrderInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV, res_dict['Token'])

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info)

return_text = EXEC_ACT(ACT_API.GetQuerMemberInfoUrl)

return_decode_text = EXEC_ACT(ACT_API.decrypt, return_text)

return_decode_dict = EXEC_ACT(ACT_API.strToDict, return_decode_text)

VERIFY(VER_API.verifyGetUserInfoFormat, return_decode_dict, CASE_NAME)

DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)