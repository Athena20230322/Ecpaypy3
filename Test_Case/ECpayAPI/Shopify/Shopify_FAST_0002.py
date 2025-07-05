# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
#from ECpay.ProdActions.ActECpayAPI.ActInvIssueb2c import actInvIssueb2c
from ECpay.ProdActions.ActECpayAPI.ActShopify import actShopify
from ECpay.Verification.VerifyECpayAPI.VerifyShopify import verifyShopify


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
#ISSUE_API = actInvIssueb2c()
ACT_API = actShopify()
VER_API = verifyShopify()


# Testing exec
# precondition-InvIssue
# INV_ISSUE_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvQueryb2c', 'Initial_Data', 'InvIssue.csv')
#
#
# inv_info = EXEC_ACT(ISSUE_API.genOrderRequestInfoB2c, INV_ISSUE_INFO_CSV)
#
# data1=EXEC_ACT(ISSUE_API.decryptDatab2c, inv_info['Data'])
#
# invoice_rtn = EXEC_ACT(ISSUE_API.genPostRequestToAPI, inv_info)
#
# res_dict = EXEC_ACT(ISSUE_API.strToDict, invoice_rtn)
#
# data = EXEC_ACT(ISSUE_API.decryptDatab2c, res_dict['Data'])

# InvQuery
SHOPIFY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'Shopify', CASE_NAME, 'ShopifyOrder.csv')

EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

shopify_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2cS, SHOPIFY_INFO_CSV)

html_path = os.path.join(ROOTDIR, 'Tmp')

query_rtn = EXEC_ACT(ACT_API.genPostRequestToAPI, html_path,shopify_info)

EXEC_ACT(ACT_API.inputPaymentPageCreditInfoShopify, '4311-9544-4444-4444', '23', '05', '222', '0900000000', 'divide','test', ' autotest123@gmail.com')

time.sleep(5)

EXEC_ACT(ACT_API.inputOTPCredit, '1234')

time.sleep(10)

QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'Shopify', CASE_NAME, 'Query.csv')

query_info = EXEC_ACT(ACT_API.genOrderRequestInfoShopify,QUERY_INFO_CSV ,shopify_info['x_reference'])

print(query_info)

order_info_res = EXEC_ACT(ACT_API.genPostRequestQueryToAPI, query_info)


res_dict = EXEC_ACT(ACT_API.strToDict, order_info_res)

print(res_dict['MerchantTradeNo'])
print(res_dict['TradeNo'])

VERIFY(VER_API.verifyInfoReturn, res_dict, CASE_NAME)


EXEC_ACT(ACT_API.cleanHtmlTmp, html_path)

time.sleep(3)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
