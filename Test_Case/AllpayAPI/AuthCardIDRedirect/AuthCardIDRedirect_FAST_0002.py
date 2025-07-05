# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActLoginPage import actLoginPage
from Allpay.ProdActions.ActAllpayAPI.ActBindingTradeRedirect import actBindingTradeRedirect
from Allpay.ProdActions.ActAllpayAPI.ActAuthCardIDRedirect import actAuthCardIDRedirect
from Allpay.Verification.VerifyAllpayAPI.VerifyAuthCardIDRedirect import verifyAuthCardIDRedirect

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
LOG_API = actLoginPage(DRIVER, SUM_LOG)
BIND_API = actBindingTradeRedirect()
ACT_API = actAuthCardIDRedirect()
VER_API = verifyAuthCardIDRedirect()

# Testing exec
# precondition-generate order
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'BindingTradeRedirect', 'Initial_Data', 'OrderInfo.csv')

EXEC_ACT(BIND_API.enableWebOperate, DRIVER)

EXEC_ACT(LOG_API.generalLogin, 'qaat0001', 'pw0001')

order_info = EXEC_ACT(BIND_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(BIND_API.createOrderByBrowser, DRIVER, order_info, 'Chkout_Jump_API')

EXEC_ACT(BIND_API.inputPaymentPageCreditInfo, '4311-9533-3333-3333', '22', '05', '222')

# precondition-query order info and get AllpayTradeNo
QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'BindingTradeRedirect', 'Initial_Data', 'QueryInfo.csv')

query_info = EXEC_ACT(BIND_API.genQueryRequestInfo, QUERY_INFO_CSV, order_info)

query_response = EXEC_ACT(BIND_API.genPostRequestToAPI, query_info, 'Query_Jump_API')

query_response_dict = EXEC_ACT(BIND_API.strToDict, query_response)

time.sleep(3)
# precondition-BindingTrade
BINDING_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'BindingTradeRedirect', 'BindingTradeRedirect_FAST_0002', 'BindingInfo.csv')

binding_info = EXEC_ACT(BIND_API.genBindingRequestInfo, BINDING_INFO_CSV, query_response_dict, '')

binding_response = EXEC_ACT(BIND_API.genPostRequestToAPI, binding_info, 'Binding_Jump_API')

# AuthCardID
AUTH_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'AuthCardIDRedirect', CASE_NAME, 'AuthInfo.csv')

auth_info = EXEC_ACT(ACT_API.genAuthRequestInfo, AUTH_INFO_CSV, '0000')

response = EXEC_ACT(ACT_API.authPostRequest, auth_info, 'Jump_Auth')

# VERIFY
VERIFY(VER_API.verifyReturnMsg, response)

DRIVER.delete_all_cookies()
DRIVER.quit()

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
