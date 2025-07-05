# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActBindingTrade import actBindingTrade
from ECpay.Verification.VerifyECpayAPI.VerifyBindingTrade import verifyBindingTrade


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
ACT_API = actBindingTrade()
VER_API = verifyBindingTrade()

# Testing exec
# precondition-generate order
ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'BindingTrade', 'Initial_Data', 'OrderInfo.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV)

EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info, 'Chkout_API')

EXEC_ACT(ACT_API.inputPaymentPageCreditInfoE, '4311-9544-4444-4444', '23', '05', '222', '0900000000', ' autotest123@gmail.com','test', '')

# precondition-query order info and get AllpayTradeNo
QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'BindingTrade', 'Initial_Data', 'QueryInfo.csv')

query_info = EXEC_ACT(ACT_API.genQueryRequestInfo, QUERY_INFO_CSV, order_info)

query_response = EXEC_ACT(ACT_API.genPostRequestToAPI, query_info, 'Query_API')

query_response_dict = EXEC_ACT(ACT_API.strToDict, query_response)

time.sleep(10)
# BindingTrade
BINDING_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'BindingTrade', CASE_NAME, 'BindingInfo.csv')

binding_info = EXEC_ACT(ACT_API.genBindingRequestInfo, BINDING_INFO_CSV, query_response_dict, '')

binding_response = EXEC_ACT(ACT_API.genPostRequestToAPI, binding_info, 'Binding_API')

binding_response_dict = EXEC_ACT(ACT_API.strToDict, binding_response)


# VERIFY
VERIFY(VER_API.verifyResponseValues, binding_response_dict, CASE_NAME, binding_info)

DRIVER.delete_all_cookies()
DRIVER.quit()


# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
