# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
#from ECpay.ProdActions.ActECpayAPI.ActInvIssueb2c import actInvIssueb2c
from ECpay.ProdActions.ActECpayAPI.ActShopify import actShopify
from ECpay.Verification.VerifyECpayAPI.VerifyShopify import verifyShopify
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper

from  ECpay.ProdActions.ActECpayAPI.ActAioCheckOut import actAioCheckOut
from ECpay.Verification.VerifyECpayAPI.VerifyAioCheckOut import verifyAioCheckOut

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

SHOPIFY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'Shopify', "Shopify_FAST_0002", 'ShopifyOrder.csv')

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


# InvQuery
SHOPIFY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'Shopify', CASE_NAME, 'ShopifyQuery.csv')

shopify_info = EXEC_ACT(ACT_API.genOrderRequestInfoSS, SHOPIFY_INFO_CSV,res_dict['MerchantTradeNo'],res_dict['TradeNo'])

query_rtn = EXEC_ACT(ACT_API.genPostRequestToAPINohtmlvoid,shopify_info)

res_dict = EXEC_ACT(ACT_API.strToDict2, query_rtn)

VERIFY(VER_API.verifyInfoReturn, res_dict, CASE_NAME)




time.sleep(3)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
