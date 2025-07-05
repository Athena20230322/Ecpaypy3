# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from Allpay.ProdActions.ActAllpayAPI.ActBindingTradeRedirect import actBindingTradeRedirect
from Allpay.Verification.VerifyAllpayAPI.VerifyBindingTradeRedirect import verifyBindingTradeRedirect
from Allpay.ProdActions.ActAllpayAPI.ActEditCardIDRedirect import actEditCardIDRedirect
from Allpay.Verification.VerifyAllpayAPI.VerifyEditCardIDRedirect import verifyEditCardIDRedirect


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
ACT_BT_API = actBindingTradeRedirect()
VER_BT_API = verifyBindingTradeRedirect()
ACT_API = actEditCardIDRedirect()
VER_API = verifyEditCardIDRedirect()

# Testing exec

# precondition-generate order
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'BindingTradeRedirect', 'Initial_Data', 'OrderJumpInfo.csv')

EXEC_ACT(ACT_BT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_BT_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_BT_API.createOrderByBrowser, DRIVER, order_info, 'Chkout_Jump_API')

EXEC_ACT(ACT_BT_API.inputRedirectPaymentPageCreditInfo, '4311-9544-4444-4444', '22', '05', '222')

# precondition-query order info and get AllpayTradeNo
QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'BindingTradeRedirect', 'Initial_Data', 'QueryJumpInfo.csv')

query_info = EXEC_ACT(ACT_BT_API.genQueryRequestInfo, QUERY_INFO_CSV, order_info)

query_response = EXEC_ACT(ACT_BT_API.genPostRequestToAPI, query_info, 'Query_Jump_API')

query_response_dict = EXEC_ACT(ACT_BT_API.strToDict, query_response)

time.sleep(3)
# BindingTradeRedirect
BINDING_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'BindingTradeRedirect',
                                'BindingTradeRedirect_RAT_0001', 'BindingInfo.csv')

binding_info = EXEC_ACT(ACT_BT_API.genBindingRequestInfo, BINDING_INFO_CSV, query_response_dict, '')

binding_response = EXEC_ACT(ACT_BT_API.genPostRequestToAPI, binding_info, 'Binding_Jump_API')

binding_response_dict = EXEC_ACT(ACT_BT_API.strToDict, binding_response)

# VERIFY
VERIFY(VER_BT_API.verifyColumns, binding_response_dict, 'BindingTradeRedirect_RAT_0001')

# EditCardID Redirect

ECID_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'AllpayAPI', 'EditCardIDRedirect', CASE_NAME, 'OrderInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

ecid_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ECID_INFO_CSV, binding_response_dict)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, ecid_info, 'EditCardID_AP_API')

EXEC_ACT(ACT_API.inputOldCreditCard4NoInfo, '4444')

EXEC_ACT(ACT_API.inputEditCreditCardInfo, '4311-9555-5555-5555', '222')

client_text = EXEC_ACT(ACT_API.GetInfoFromClientRedirectUrl)

client_dict = EXEC_ACT(ACT_API.redirectStrToDict, client_text)

# VERIFY

VERIFY(VER_API.verifyClientRedirectColumns, client_dict, CASE_NAME)

DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)