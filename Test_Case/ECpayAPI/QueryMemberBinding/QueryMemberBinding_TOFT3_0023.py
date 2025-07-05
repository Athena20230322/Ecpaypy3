# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActTradeWithBindingCardID import actTradeWithBindingCardID
from ECpay.Verification.VerifyECpayAPI.VerifyTradeWithBindingCardID import verifyTradeWithBindingCardID
from ECpay.ProdActions.ActECpayAPI.ActQueryMemberBinding import actQueryMemberBinding
from ECpay.Verification.VerifyECpayAPI.VerifyQueryMemberBinding import verifyQueryMemberBinding


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
ACT_TWBCID_API = actTradeWithBindingCardID()
VER_TWBCID_API = verifyTradeWithBindingCardID()
ACT_API = actQueryMemberBinding()
VER_API = verifyQueryMemberBinding()

# Precondition TradeWithBindingCardID

# BIND_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'TradeWithBindingCardID', 'TradeWithBindingCardID_RAT_0001', 'BindingInfo.csv')

# EXEC_ACT(ACT_TWBCID_API.enableWebOperate, DRIVER)

# bind_info = EXEC_ACT(ACT_TWBCID_API.genBindingRequestInfo, BIND_INFO_CSV)

# EXEC_ACT(ACT_TWBCID_API.bindingByBrowser, DRIVER, bind_info)

# EXEC_ACT(ACT_TWBCID_API.inputCreditInfo, '4311-9544-4444-4444', '222')

# response = EXEC_ACT(ACT_TWBCID_API.GetInfoFromServerReplyUrl, bind_info['MerchantTradeNo'])

# client_text = EXEC_ACT(ACT_TWBCID_API.GetInfoFromClientRedirectUrl)

# client_dict = EXEC_ACT(ACT_TWBCID_API.redirectStrToDict, client_text)

# Precondition Verify TradeWithBindingCardID

# VERIFY(VER_TWBCID_API.verifyServerReplyColumns, response, 'TradeWithBindingCardID_RAT_0001')

# VERIFY(VER_TWBCID_API.verifyClientRedirectColumns, client_dict, 'TradeWithBindingCardID_RAT_0001')

# Testing exec

ORDER_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'QueryMemberBinding', CASE_NAME, 'OrderInfo.csv')

# EXEC_ACT(ACT_API.enableWebOperate, DRIVER)

order_info = EXEC_ACT(ACT_API.genOrderRequestInfo, ORDER_INFO_CSV, 'sleep(__TIME__)#')

# EXEC_ACT(ACT_API.createOrderByBrowser, DRIVER, order_info)

order_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, order_info)

# print order_info_res_dict

VERIFY(VER_API.verifyStatusResult, order_info_res, 'MerchantMemberID=sleep(__TIME__)#&Count=0')

# DRIVER.delete_all_cookies()
# DRIVER.quit()

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)